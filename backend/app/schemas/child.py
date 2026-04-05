from datetime import date
from typing import Optional
from fastapi.openapi.models import Operation
from pydantic import BaseModel
from app.models.child import GenderEnum

# こども情報登録時スキーマ
class ChildCreate(BaseModel):
    name: str
    gender: Optional[GenderEnum] = None
    birthday: date
    weight: Optional[float] = None
    chronic_disease: Optional[str] = None
    allergy: Optional[str] = None

#こども情報更新時スキーマ
class ChildUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    birthday: Optional[date] = None
    weight: Optional[float] = None
    chronic_disease: Optional[str] = None
    allergy: Optional[str] = None

# レスポンス用スキーマ
class ChildResponse(BaseModel):
    id: int
    name: str
    gender: Optional[GenderEnum] = None
    birthday: date
    weight: Optional[float] = None
    chronic_disease: Optional[str] = None
    allergy: Optional[str] = None

    class Config:
        from_attributes = True