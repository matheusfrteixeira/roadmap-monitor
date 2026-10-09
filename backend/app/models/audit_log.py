from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String(20), nullable=False)  # INSERT, UPDATE, DELETE
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User")

