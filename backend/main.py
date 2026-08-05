from fastapi import FastAPI
from app.routers import auth, children, hospitals, visits, visit_image, departments

# appインスタンスを作成（サーバ本体）
app = FastAPI()

# ルートURLにアクセスしたときの処理
@app.get("/")
def read_root():
    return {"message": "Famicul API is running!"}

# ログイン処理の読み込み
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# /childrenへのアクセスの処理
app.include_router(children.router, tags=["children"])

# /hospitalsへのアクセスの処理
app.include_router(hospitals.router, tags=["hospitals"])

# /visitsへのアクセスの処理
app.include_router(visits.router, tags=["visits"])

# /children/{child_id}/visits/{id}/imagesへのアクセス処理
app.include_router(visit_image.router, tags=["visit-images"])

# /departmentsへのアクセス
app.include_router(departments.router, tags=["departments"])
