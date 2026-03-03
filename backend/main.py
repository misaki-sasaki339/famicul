from fastapi import FastAPI
from app.database import engine, Base
from app.models import hospital

# テーブルがない場合作成する
Base.metadata.create_all(bind=engine)

# appインスタンスを作成（サーバ本体）
app = FastAPI()

# ルートURLにアクセスしたときの処理
@app.get("/")
def read_root():
    return {"message": "Hospital table created!"}