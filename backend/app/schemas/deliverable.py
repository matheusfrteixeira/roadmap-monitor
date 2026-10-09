from typing import Optional, List
from pydantic import BaseModel
from datetime import date

class DeliverableBase(BaseModel):
    name: str
    description: Optional[str] = None
    comments: Optional[str] = None
    status: str = "Não Iniciado"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    progress: float = 0.0
    project_id: int

class DeliverableCreate(DeliverableBase):
    pass

class DeliverableUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    comments: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    progress: Optional[float] = None

class DeliverableResponse(DeliverableBase):
    id: int
    total_activities: int = 0
    completed_activities: int = 0
    delayed_activities: int = 0
    total_tracked_minutes: int = 0
    total_tracked_hours: float = 0.0

    class Config:
        from_attributes = True

