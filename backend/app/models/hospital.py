from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255))
    tel = Column(String(20))
    memo = Column(Text)