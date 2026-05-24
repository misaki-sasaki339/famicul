from sqlalchemy.orm import Session
from app.models.visit import VisitImage

# 受診IDに紐づく画像を新規作成する
def create_visit_image(
    db: Session,
    visit_id: int,
    storage_key: str
) -> VisitImage:
    # ローカル保存したパスをDBに保存
    new_visit_image = VisitImage(
        visit_id=visit_id,
        s3_key=storage_key
    )

    # DBに追加して保存
    db.add(new_visit_image)
    db.commit()
    db.refresh(new_visit_image)

    # 作成した画像情報を返す
    return new_visit_image

# 受診IDに紐づく画像一覧を取得する
def get_visit_images_by_visit_id(
    db: Session,
    visit_id: int
) -> list[VisitImage]:
    # 対象の受診IDに紐づく画像を全件取得する
    visit_images = db.query(VisitImage).filter(VisitImage.visit_id == visit_id).all()

    # 取得した画像を返す
    return visit_images

# 画像IDと受診IDで画像を１件取得する
def get_visit_image_by_id_and_visit_id(
    db: Session,
    visit_id: int,
    image_id: int
) -> VisitImage | None:
    # URLのvisit_idとimage_idが一致する画像１件を取得する
    return (
        db.query(VisitImage)
        .filter(VisitImage.id == image_id, VisitImage.visit_id == visit_id)
        .first()
    )

# 画像１件を削除する
def delete_visit_image(
    db: Session,
    visit_image: VisitImage
) -> None:
    # 渡された画像レコードを削除して確定
    db.delete(visit_image)
    db.commit()