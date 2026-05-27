from fastapi import FastAPI
from app.routers import auth
from app.routers import children
from app.routers import hospitals
from app.routers import visits
from app.routers import visit_image

# appインスタンスを作成（サーバ本体）
app = FastAPI()

# ルートURLにアクセスしたときの処理
@app.get("/")
def read_root():
    return {"message": "Famicul API is running!"}

# ログイン処理の読み込み
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# /childへのアクセスの処理
app.include_router(children.router, tags=["children"])

# /hospitalへのアクセスの処理
app.include_router(hospitals.router, tags=["hospital"])

# /visitsへのアクセスの処理
app.include_router(visits.router, tags=["visit"])

# /children/{child_id}/visits/{id}/imagesへのアクセス処理
app.include_router(visit_image.router, tags=["visit-images"])