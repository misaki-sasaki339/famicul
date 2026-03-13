from pydantic import BaseModel

# 病名・症状名登録時のスキーマ
class DiseaseCreate(BaseModel):
    name: str