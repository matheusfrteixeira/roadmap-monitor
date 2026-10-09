from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class ActiveTimer(Base):
    __tablename__ = "active_timers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, index=True)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user = relationship("User")
    activity = relationship("Activity")

