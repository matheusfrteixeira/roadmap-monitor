from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.time_entry import (
    TimeEntryCreate,
    TimeEntryResponse,
    ActiveTimerStart,
    ActiveTimerStop,
    ActiveTimerResponse
)
from app.services.time_entry_service import TimeEntryService

router = APIRouter()

@router.get("/active", response_model=Optional[ActiveTimerResponse])
def get_active_timer(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Retorna o cronômetro atualmente em execução do usuário autenticado."""
    service = TimeEntryService(db)
    return service.get_active_timer(current_user)

@router.post("/start", response_model=ActiveTimerResponse)
def start_active_timer(
    payload: ActiveTimerStart,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Inicia o cronômetro do usuário na atividade.
    Se já existir cronômetro rodando em outra atividade, finaliza e grava automaticamente.
    """
    service = TimeEntryService(db)
    return service.start_active_timer(payload.activity_id, current_user)

@router.post("/stop", response_model=TimeEntryResponse)
def stop_active_timer(
    payload: ActiveTimerStop,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Para o cronômetro ativo do usuário e grava o apontamento no banco de dados.
    """
    service = TimeEntryService(db)
    return service.stop_active_timer(payload.description, current_user)

@router.post("/", response_model=TimeEntryResponse)
def log_time(
    time_in: TimeEntryCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = TimeEntryService(db)
    return service.log_time(time_in, current_user)

@router.get("/me", response_model=List[TimeEntryResponse])
def get_my_time_entries(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = TimeEntryService(db)
    return service.get_my_time_entries(current_user.id)

@router.get("/activity/{activity_id}", response_model=List[TimeEntryResponse])
def get_activity_time_entries(
    activity_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = TimeEntryService(db)
    return service.get_activity_time_entries(activity_id)

@router.get("/activity/{activity_id}/total")
def get_activity_total_time(
    activity_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    service = TimeEntryService(db)
    return service.get_activity_total_time(activity_id)

@router.get("/calendar")
def get_calendar_time_entries(
    user_id: Optional[int] = Query(None, description="Filtrar por usuário específico se permitido"),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Visão de acompanhamento/calendário de apontamentos.
    - Analista: vê apenas os seus próprios apontamentos.
    - Gestor: vê os seus apontamentos e de todos os seus subordinados.
    - Admin: vê de qualquer usuário.
    """
    service = TimeEntryService(db)
    return service.get_calendar_entries(current_user, target_user_id=user_id)

@router.get("/project/{project_id}")
def get_project_time_summary(
    project_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retorna histórico e total de horas apontadas na demanda por membro da equipe.
    """
    service = TimeEntryService(db)
    return service.get_project_time_summary(project_id)
