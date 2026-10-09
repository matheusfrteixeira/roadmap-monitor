from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, RoleEnum
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([RoleEnum.admin]))
):
    """Cria novo usuário (Apenas Admin)."""
    service = UserService(db)
    return service.create_user(user_in)

@router.get("/me", response_model=UserResponse)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Retorna dados do usuário logado."""
    service = UserService(db)
    user = service.get_user_by_email(current_user.email)
    return user or current_user

@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    """Lista usuários (todos autenticados podem ver para preencher selects)."""
    service = UserService(db)
    return service.get_all_users()

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([RoleEnum.admin]))
):
    """Atualiza dados do usuário, perfil e gestor imediato (Apenas Admin)."""
    service = UserService(db)
    return service.update_user(user_id, user_in)
