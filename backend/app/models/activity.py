from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    status = Column(String(50), default="Não Iniciado")
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    progress = Column(Float, default=0.0)
    
    project_id = Column(Integer, ForeignKey("projects.id"))
    deliverable_id = Column(Integer, ForeignKey("deliverables.id", ondelete="SET NULL"), nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    project = relationship("Project", back_populates="activities")
    deliverable = relationship("Deliverable", back_populates="activities")
    assignee = relationship("User", foreign_keys=[assignee_id])
