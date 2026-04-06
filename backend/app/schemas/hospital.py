from typing import Optional
from pydantic import BaseModel

# 病院登録時スキーマ
class HospitalCreate(BaseModel):
    name: str
    address: Optional[str] = None
    tel: Optional[str] = None
    memo: Optional[str] = None

# 病院情報更新時スキーマ
class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    tel: Optional[str] = None
    memo: Optional[str] = None

# レスポンス用スキーマ
class HospitalResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    tel: Optional[str] = None
    memo: Optional[str] = None

    class Config:
        from_attributes = True