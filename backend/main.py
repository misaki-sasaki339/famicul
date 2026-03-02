from fastapi import FastAPI

# appインスタンスを作成（サーバ本体）
app = FastAPI()

# ルートURLにアクセスしたときの処理
@app.get("/")
def read_root():
    return {"message": "Hello Famicul! 準備OK!"}

# 疎通確認用のテスとエンドポイント
@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "waiting..."}
