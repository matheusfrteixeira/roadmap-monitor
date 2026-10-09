from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.deliverable import DeliverableCreate, DeliverableResponse, DeliverableUpdate
from app.services.deliverable_service import DeliverableService

router = APIRouter()

@router.get("/", response_model=List[DeliverableResponse])
def get_all_deliverables(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = DeliverableService(db)
    return service.get_all()

@router.get("/project/{project_id}", response_model=List[DeliverableResponse])
def get_deliverables_by_project(
    project_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = DeliverableService(db)
    return service.get_by_project(project_id)

@router.get("/{deliverable_id}", response_model=DeliverableResponse)
def get_deliverable(
    deliverable_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = DeliverableService(db)
    return service.get_by_id(deliverable_id)

@router.post("/", response_model=DeliverableResponse)
def create_deliverable(
    deliverable_in: DeliverableCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = DeliverableService(db)
    return service.create_deliverable(deliverable_in)

@router.put("/{deliverable_id}", response_model=DeliverableResponse)
def update_deliverable(
    deliverable_id: int,
    deliverable_in: DeliverableUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = DeliverableService(db)
    return service.update_deliverable(deliverable_id, deliverable_in)

@router.delete("/{deliverable_id}")
def delete_deliverable(
    deliverable_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = DeliverableService(db)
    service.delete_deliverable(deliverable_id)
    return {"message": "Entregável excluído com sucesso."}

