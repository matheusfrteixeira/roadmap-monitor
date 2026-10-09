from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Deliverable(Base):
    __tablename__ = "deliverables"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    status = Column(String(50), default="Não Iniciado")
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    progress = Column(Float, default=0.0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="deliverables")
    activities = relationship("Activity", back_populates="deliverable", cascade="all, delete-orphan")

