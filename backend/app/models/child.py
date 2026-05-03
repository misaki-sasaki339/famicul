import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Enum, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

from app.database import Base

# PythonのEnumクラスを定義
class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    
class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=True)
    birthday = Column(Date)
    weight = Column(Float)
    #既往歴、アレルギー情報は記述が増えることも想定してText型
    chronic_disease = Column(Text, nullable=True)
    allergy = Column(Text, nullable=True)
    memo = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーションの定義
    user = relationship("User", back_populates="children")
    visits = relationship("Visit", back_populates="child")