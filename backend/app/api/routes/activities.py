from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.services.activity_service import ActivityService

router = APIRouter()

@router.get("/", response_model=List[ActivityResponse])
def get_activities(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    service = ActivityService(db)
    return service.get_all_activities()

@router.post("/", response_model=ActivityResponse)
def create_activity(
    activity_in: ActivityCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = ActivityService(db)
    return service.create_activity(activity_in)

@router.put("/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: int,
    activity_in: ActivityUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = ActivityService(db)
    return service.update_activity(activity_id, activity_in, current_user)

@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = ActivityService(db)
    service.delete_activity(activity_id, current_user)
    return {"message": "Atividade excluída com sucesso."}
