from sqlalchemy.orm import Session, selectinload, joinedload
from app.models import Visit
from app.models.disease import Disease, VisitDisease
from app.schemas.visit import VisitCreate, VisitUpdate

# 病名リストを正規化（空白除去、空文字除去、重複削除）する
def _normalized_disease_names(disease_names: list[str] | None):
    normalized_names: list[str] = []

    for disease_name in disease_names or []:
        # 前後の空白を削除する
        normalized_name = disease_name.strip()

        # 空文字でない、かつまだ追加していない病名だけを追加する
        if normalized_name and normalized_name not in normalized_names:
            normalized_names.append(normalized_name)

    return normalized_names

# 受診記録に紐づく病名を一度全削除して最新を入れ直す
def _replace_visit_diseases(
    db: Session,
    visit: Visit,
    disease_names: list[str] | None
) -> None:
    # 対象visitの既存の中間テーブル行を削除する
    db.query(VisitDisease).filter(VisitDisease.visit_id == visit.id).delete()

    # 正規化した病名一覧をつくる
    normalized_names = _normalized_disease_names(disease_names)

    for disease_name in normalized_names:
        # disease_nameがすでにDiseaseテーブルに存在するか探す
        disease = db.query(Disease).filter(Disease.name == disease_name).first()
    
        if not disease:
            # なければDiseaseオブジェクトを生成して追加
            disease = Disease(name=disease_name)
            db.add(disease)

            # 新規のdiseaseにはdisease.idが付与されていないためflush(一時保存)して採番
            db.flush()

        # visitとdiseaseの紐付けを中間テーブルへ追加する
        db.add(VisitDisease(
            visit_id=visit.id,
            disease_id=disease.id
        ))

# こどもIDに紐づく受診記録を全件取得
def list_visits_by_child_id_with_diseases(
    db: Session,
    child_id: int
) -> list[Visit]:
    # Visitテーブルからchild_idが一致するものを受診日降順で表示
    return (
        db.query(Visit)
        .filter(Visit.child_id == child_id)
        .options(selectinload(Visit.disease_links).selectinload(VisitDisease.disease))
        .order_by(Visit.visit_date.desc())
        .all()
    )

# こどもIDと受診記録IDから受診記録を取得
def get_visit_by_id_and_child_id_with_disease(
    db: Session,
    child_id: int,
    visit_id: int
):
    return (
        db.query(Visit)
        .filter(Visit.id == visit_id, Visit.child_id == child_id)
        .options(joinedload(Visit.disease_links).joinedload(VisitDisease.disease))
        .first()
    )

# 受診記録の新規作成
def create_visit(
    db: Session,
    child_id: int,
    visit_in: VisitCreate
):
    # 入力データから受診記録モデルを作成して保存する
    new_visit = Visit(
        child_id = child_id,
        hospital_id = visit_in.hospital_id,
        department_id = visit_in.department_id,
        visit_date = visit_in.visit_date,
        symptom = visit_in.symptom,
        advice = visit_in.advice,
        next_visit_at = visit_in.next_visit_at,
        is_emergency = visit_in.is_emergency
    )
    db.add(new_visit)

    # visit_idを確定させるためflushする
    db.flush()

    # disease_namesを中間テーブルに保存する
    _replace_visit_diseases(db, new_visit, visit_in.disease_names)

    db.commit()
    db.refresh(new_visit)

    return new_visit

# 受診記録の更新
def update_visit(
    db: Session,
    visit: Visit,
    visit_in: VisitUpdate
):
    update_data = visit_in.model_dump(exclude_unset=True)

    # update_dataからdisease_namesを取り出す（なければNone）
    disease_names = update_data.pop("disease_names", None)

    for key, value in update_data.items():
        setattr(visit, key, value)

    # disease_namesが指定されている時だけ中間テーブルを更新
    if disease_names is not None:
        _replace_visit_diseases(db, visit, disease_names)

    db.commit()
    db.refresh(visit)

    return visit

# 受診記録の削除
def delete_visit(
    db: Session,
    visit: Visit
) -> None:
    db.delete(visit)
    db.commit()
    # 削除が実行されるとdbから削除されるためrefresh(visit)は不要