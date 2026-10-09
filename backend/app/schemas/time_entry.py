from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TimeEntryBase(BaseModel):
    time_spent_minutes: int
    description: Optional[str] = None
    activity_id: int

class TimeEntryCreate(TimeEntryBase):
    pass

class TimeEntryResponse(TimeEntryBase):
    id: int
    user_id: int
    date_recorded: datetime

    class Config:
        from_attributes = True

class ActiveTimerStart(BaseModel):
    activity_id: int

class ActiveTimerStop(BaseModel):
    description: Optional[str] = None

class ActiveTimerResponse(BaseModel):
    id: int
    user_id: int
    activity_id: int
    activity_name: Optional[str] = None
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    start_time: str
    elapsed_seconds: int = 0

    class Config:
        from_attributes = True

