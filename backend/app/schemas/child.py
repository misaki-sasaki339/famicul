from datetime import date
from typing import Optional
from pydantic import BaseModel

from app.models.child import GenderEnum
# こども情報登録時のスキーマ
class ChildCreate(BaseModel):
    name: str
    gender: Optional[GenderEnum] = None
    birthday: date
    weight: Optional[float] = None
    chronic_disease: Optional[str] = None
    allergy: Optional[str] = None
