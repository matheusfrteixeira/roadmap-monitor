from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    service = ProjectService(db)
    return service.get_all_projects()

@router.post("/", response_model=ProjectResponse)
def create_project(
    project_in: ProjectCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = ProjectService(db)
    return service.create_project(project_in)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = ProjectService(db)
    return service.update_project(project_id, project_in)
