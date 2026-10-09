from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    priority = Column(String(50), default="Normal")
    status = Column(String(50), default="Não Iniciado")
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    progress = Column(Float, default=0.0)

    ticket_number = Column(String(50), nullable=True)
    requester = Column(String(150), nullable=True)
    comments = Column(Text, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    area_id = Column(Integer, ForeignKey("areas.id"), nullable=True)
    
    owner = relationship("User", foreign_keys=[owner_id])
    area = relationship("Area")
    deliverables = relationship("Deliverable", back_populates="project", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="project", cascade="all, delete-orphan")
