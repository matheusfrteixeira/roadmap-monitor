from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Area(Base):
    __tablename__ = "areas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

