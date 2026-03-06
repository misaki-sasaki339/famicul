from fastapi import FastAPI
from app.database import engine, Base
from app.models import hospital

# appインスタンスを作成（サーバ本体）
app = FastAPI()

# ルートURLにアクセスしたときの処理
@app.get("/")
def read_root():
    return {"message": "Hospital table created!"}