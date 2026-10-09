from typing import Optional
from pydantic import BaseModel
from datetime import date

class ProjectBase(BaseModel):
    name: str
    priority: str = "Normal"
    status: str = "Não Iniciado"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    progress: float = 0.0
    ticket_number: Optional[str] = None
    requester: Optional[str] = None
    comments: Optional[str] = None
    area_id: Optional[int] = None
    owner_id: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    progress: Optional[float] = None
    ticket_number: Optional[str] = None
    requester: Optional[str] = None
    comments: Optional[str] = None
    area_id: Optional[int] = None
    owner_id: Optional[int] = None

class ProjectResponse(ProjectBase):
    id: int
    total_deliverables: int = 0
    total_activities: int = 0
    completed_activities: int = 0
    delayed_activities: int = 0
    total_tracked_minutes: int = 0
    total_tracked_hours: float = 0.0
    area_name: Optional[str] = None
    owner_name: Optional[str] = None
    manager_id: Optional[int] = None
    manager_name: Optional[str] = None

    class Config:
        from_attributes = True
