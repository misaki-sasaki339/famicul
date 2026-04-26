from sqlalchemy.orm import Session
from app.models import Visit
from app.models.disease import Disease, VisitDisease
from app.schemas.visit import VisitCreate, VisitUpdate

def _normalize_disease_names(disease_names: list[str] | None) -> list[str]:
    # 前後の空白を削除し、空文字と重複を除いた病名リストを作る
    normalized_names: list[str] = []
    for disease_name in disease_names or []:
        normalized_name = disease_name.strip()
        if normalized_name and normalized_name not in normalized_names:
            normalized_names.append(normalized_name)
    return normalized_names


def _replace_visit_diseases(
    db: Session,
    visit: Visit,
    disease_names: list[str] | None
) -> None:
    # 既存の紐付けをいったん全削除して最新の病名一覧で作り直す
    db.query(VisitDisease).filter(VisitDisease.visit_id == visit.id).delete()

    # 入力病名を正規化して保存対象を確定する
    normalized_names = _normalize_disease_names(disease_names)

    for disease_name in normalized_names:
        # 病名マスタにすでに存在するか確認する
        disease = db.query(Disease).filter(Disease.name == disease_name).first()
        if not disease:
            # 未登録病名はマスタへ追加する
            disease = Disease(name=disease_name)
            db.add(disease)
            db.flush()

        # 受診記録と病名の紐付けを中間テーブルへ登録する
        db.add(VisitDisease(visit_id=visit.id, disease_id=disease.id))

# こどもIDと受診記録IDから受診記録を取得
def get_visit_by_id_and_child_id(
    db: Session,
    child_id: int,
    visit_id: int
):
    return db.query(Visit).filter(Visit.id == visit_id, Visit.child_id == child_id).first()

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
    # 受診記録ID確定後に病名紐付けを保存するためflushする
    db.flush()
    # 病名マスタと中間テーブルの保存を行う
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

    # disease_namesは受診記録本体ではなく中間テーブル側で扱う
    disease_names = update_data.pop("disease_names", None)

    for key, value in update_data.items():
        setattr(visit, key, value)

    # disease_namesがリクエストに含まれていた場合のみ病名紐付けを更新する
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