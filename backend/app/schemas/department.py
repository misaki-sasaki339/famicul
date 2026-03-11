from pydantic import BaseModel

# 診療科登録時のスキーマ
class DepartmentCreate(BaseModel):
    name: str