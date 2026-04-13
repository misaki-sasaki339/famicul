from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List

# --- Visit 用のスキーマ ---
# 受診履歴登録時のスキーマ
class VisitCreate(BaseModel):
    child_id: int
    hospital_id: int
    department_id: int
    visit_date: date
    symptom: str
    advice: Optional[str] = None
    next_visit_at: Optional[datetime] = None
    is_emergency: Optional[bool] = False
    # 呼び出ごとに新しいリストを作成
    disease_names: List[str] = Field(default_factory=list)

# --- VisitImage 用のスキーマ ---
# 受診履歴に紐づく画像データ登録時のスキーマ
class VisitImageCreate(BaseModel):
    visit_id: int
    s3_key:str