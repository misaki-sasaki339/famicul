from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Visit
from app.crud import visit as visit_crud
from app.schemas.visit import VisitCreate, VisitKey, VisitUpdate, VisitResponse
from app.models.child import Child

# こどもIDが存在するか確認するヘルパー関数
def _get_child_or_404(db: Session, child_id: int):
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

# 受診記録が存在するか確認するヘルパー関数
def _get_visit_or_404(
    db: Session,
    key: VisitKey
):
    # DBから対象のこどもの受診記録を取得する
    visit = visit_crud.get_visit_by_id_and_child_id_with_disease(db, key.child_id, key.visit_id)

    # 見つからない場合は404を返す
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    # 見つかった受診記録を返す
    return visit

# 受診記録の取得処理
def get_visit_service(
    db: Session,
    key: VisitKey
):
    # 共通関数を使って取得
    return to_visit_response(_get_visit_or_404(db, key))

# こどもごとの受診記録全件取得処理
def list_visits_service(
    db: Session,
    child_id: int
):
    _get_child_or_404(db, child_id)
    # DBからVisitの一覧を取得する
    visits = visit_crud.list_visits_by_child_id_with_diseases(db, child_id)
    # それぞれVisitResponseに変換して返す
    return [to_visit_response(v) for v in visits]

# 受診記録作成処理
def create_visit_service(
    db: Session,
    child_id: int,
    visit_in: VisitCreate
):
    _get_child_or_404(db, child_id)
    # DB保存処理をcrudへ委譲
    return to_visit_response(visit_crud.create_visit(db, child_id, visit_in))

# 受診記録更新処理
def update_visit_service(
    db: Session,
    key: VisitKey,
    visit_in: VisitUpdate
):
    # DBから対象のこどもの受診記録を探す
    visit = _get_visit_or_404(db, key)

    # DB保存処理をcrudへ委譲
    updated = visit_crud.update_visit(db, visit, visit_in)
    return to_visit_response(updated)

# 情報削除処理
def delete_visit_service(
    db: Session,
    key: VisitKey
):
    # DBから対象のこどもの受診記録を探す
    visit = _get_visit_or_404(db, key)
    
    # DB削除処理をcrudに委譲
    visit_crud.delete_visit(db, visit)
    return {"message": "Visit deleted successfully!"}

# visitからdisease_namesをつくる関数
def build_disease_names(visit: Visit) -> list[str]:
    # 病名を入れる箱を作る
    names: list[str] = []
    # 中間テーブルのリンクを1件ずつチェック
    for disease_link in visit.disease_links:
        # diseaseがありnameもあるときだけ追加
        if disease_link.disease and disease_link.disease.name:
            names.append(disease_link.disease.name)
    return names

# 1件のVisitをAPI返却用(VisitResponse)に変換する
def to_visit_response(visit: Visit) -> VisitResponse:
    return VisitResponse(
        id=visit.id,
        child_id=visit.child_id,
        hospital_id=visit.hospital_id,
        department_id=visit.department_id,
        symptom=visit.symptom,
        visit_date=visit.visit_date,
        advice=visit.advice,
        next_visit_at=visit.next_visit_at,
        is_emergency=visit.is_emergency,
        disease_names=build_disease_names(visit)
    )