import datetime
from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# 診療科登録時のスキーマ
class VisitCreate(BaseModel):
    child_id: int
    hospital_id: int
    department_id: int
    visit_date: date
    symptom: str
    advice: Optional[str] = None
    next_visit_at: Optional[datetime] = None
    is_emergency: Optional[bool] = False
    disease_ids: List[int] = []