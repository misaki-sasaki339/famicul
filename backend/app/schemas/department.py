from pydantic import BaseModel, ConfigDict

# 診療科登録時のスキーマ
class DepartmentCreate(BaseModel):
    name: str

# レスポンス用スキーマ
class DepartmentResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)