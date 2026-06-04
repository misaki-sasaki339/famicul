import uuid
import shutil
from pathlib import Path
from fastapi import HTTPException, UploadFile

# 保存先ルート(画像ファイルから3つ上のbackend/uploadsを指定、.resolve()を呼んで絶対パスに変換)
UPLOAD_ROOT = Path(__file__).resolve().parent.parent.parent / "uploads"
RESOLVED_UPLOAD_ROOT = UPLOAD_ROOT.resolve()

# 許可する画像形式(Content-Type → 拡張子)
ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png"
}

# 画像ファイルがuploadsディレクトリ以下にある安全な場所かをチェックする関数
def _is_under_upload_root(absolute_path: Path) -> bool:
    return RESOLVED_UPLOAD_ROOT in absolute_path.parents

# アップロードディレクトリのパスチェック関数
def _resolve_path_under_upload_root(relative_path: str | Path) -> Path:
    absolute_path = (UPLOAD_ROOT / relative_path).resolve()
    if not _is_under_upload_root(absolute_path):
        raise HTTPException(status_code=400, detail="Invalid storage path")
    return absolute_path

# 拡張子を決める関数
def _extension_for(file: UploadFile) -> str:
    #file.content_typeから拡張子を返す
    extension = ALLOWED_CONTENT_TYPES.get(file.content_type or "")
    if not extension:
        raise HTTPException(status_code=400, detail="Unsupported image type")
    return extension
    
# 画像ファイルの保存
def save_visit_image_file(visit_id: int, file: UploadFile) -> str:
    # 保存先ディレクトリの作成
    visit_dir = UPLOAD_ROOT / "visits" / str(visit_id)
    # 上位ディレクトリがなければ作成、すでに存在していてもOK
    visit_dir.mkdir(parents=True, exist_ok=True)

    # ファイル名が重複しないようUUIDを使用
    filename = f"{uuid.uuid4().hex}{_extension_for(file)}"
    destination = visit_dir / filename

    # ファイルを書き込む(w=write,b=バイナリーモード)
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # DBに入れる相対パス
    return str(destination.relative_to(UPLOAD_ROOT))

# 画像ファイルのパス解決(GET用)
def resolve_storage_path(storage_key: str) -> Path:
    absolute_path = _resolve_path_under_upload_root(storage_key)

    # ファイルがなければ404
    if not absolute_path.is_file():
        raise HTTPException(status_code=404, detail="Image file not found")

    return absolute_path

# 画像ファイルの削除(DELETE用)
def delete_storage_file(storage_key: str) -> None:
    file_path = (UPLOAD_ROOT / storage_key).resolve()

    # 不正なパスの場合は画像ファイルを削除しない
    if not _is_under_upload_root(file_path):
        return

    if file_path.is_file():
        file_path.unlink()

# 画像ファイルのディレクトリを削除
def delete_visit_upload_dir(visit_id: int) -> None:
    visit_dir = (UPLOAD_ROOT / "visits" / str(visit_id)).resolve()

    if not _is_under_upload_root(visit_dir):
        return

    if visit_dir.is_dir():
        shutil.rmtree(visit_dir)