from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Disease(Base):
    """
    病名マスタテーブル
    ユーザーが入力した病名が自動登録される（動的追加）
    """
    __tablename__ = "diseases"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーションの定義
    visit_links = relationship("VisitDisease", back_populates="disease")

class VisitDisease(Base):
    """
    Visit(受診履歴)とDisease（病名）をつなぐ中間テーブル
    1回の受診で複数の病名・症状がある状態を実現
    """
    __tablename__ = "visit_diseases"

    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーションの定義
    # 特定の１つの受診履歴・病名に紐づくので単数形を使う
    visit = relationship("Visit", back_populates="disease_links")
    disease = relationship("Disease", back_populates="visit_links")