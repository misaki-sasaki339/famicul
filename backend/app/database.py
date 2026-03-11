from sqlalchemy.orm.session import Session

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# .envからDATABASE_URLを取得
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# DBエンジン（接続の土台）を作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# DBセッションの設定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()

# DBセッションを取得する依存関数
# リクエストごとにセッションを作成し、処理終了後にクローズする
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()