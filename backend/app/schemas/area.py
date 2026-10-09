from pydantic import BaseModel
from typing import Optional

class AreaBase(BaseModel):
    name: str

class AreaCreate(AreaBase):
    pass

class AreaUpdate(BaseModel):
    name: str

class AreaResponse(AreaBase):
    id: int

    class Config:
        from_attributes = True

