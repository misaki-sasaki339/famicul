from typing import Text
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    visit_date = Column(Date, nullable=False)
    symptom = Column(String(255), nullable=False)
    advice = Column(Text)
    next_visit_at = Column(DateTime(timezone=True))
    is_emergency = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーションの定義
    child = relationship("Child", back_populates="visits")
    department = relationship("Department", back_populates="visits")
    disease_links = relationship("VisitDisease", back_populates="visit")
    hospital = relationship("Hospital", back_populates="visits")
    visit_images = relationship("VisitImage", back_populates="visit", cascade="all, delete-orphan")

class VisitImage(Base):
    __tablename__ = "visit_images"
    """
    受診履歴に紐づく患部、処方箋などの画像を管理するテーブル
    S3への保存を前提
    """

    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)

    # S3上のオブジェクトキー（例： visits/1/image.jpg）
    s3_key = Column(String(512), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーションの定義
    visit = relationship("Visit", back_populates="visit_images")