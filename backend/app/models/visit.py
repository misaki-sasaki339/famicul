from sqlite3 import Date
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
    diseases = relationship("VisitDisease", back_populates="visit")
    hospital = relationship("Hospital", back_populates="visits")
    #visit_images = relationship("Visit_Images", back_populates="visit")