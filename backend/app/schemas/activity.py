from typing import Optional
from pydantic import BaseModel
from datetime import date

class ActivityBase(BaseModel):
    name: str
    description: Optional[str] = None
    comments: Optional[str] = None
    status: str = "Não Iniciado"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    progress: float = 0.0
    project_id: int
    deliverable_id: Optional[int] = None
    assignee_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    comments: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    progress: Optional[float] = None
    deliverable_id: Optional[int] = None
    assignee_id: Optional[int] = None

class ActivityResponse(ActivityBase):
    id: int
    assignee_name: Optional[str] = None
    deliverable_name: Optional[str] = None
    is_delayed: bool = False
    total_tracked_minutes: int = 0
    total_tracked_hours: float = 0.0

    class Config:
        from_attributes = True
