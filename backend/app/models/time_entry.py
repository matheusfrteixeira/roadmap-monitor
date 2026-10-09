from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class TimeEntry(Base):
    __tablename__ = "time_entries"
    id = Column(Integer, primary_key=True, index=True)
    time_spent_minutes = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    date_recorded = Column(DateTime, default=datetime.utcnow)
    
    activity_id = Column(Integer, ForeignKey("activities.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    activity = relationship("Activity")
    user = relationship("User")

