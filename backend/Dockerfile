# Pythonの軽量版を使う（必要なものは後からインストールすればOK）
FROM python:3.11-slim

# コンテナ内の作業ディレクトリ
WORKDIR /app

# 必要なライブラリをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# FastAPIの起動コマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

