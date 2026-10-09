from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, RoleEnum
from app.schemas.area import AreaCreate, AreaUpdate, AreaResponse
from app.services.area_service import AreaService

router = APIRouter()

@router.get("/", response_model=List[AreaResponse])
def get_areas(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    """Lista todas as áreas/clientes (disponível para todos os usuários logados preencherem selects)."""
    service = AreaService(db)
    return service.get_all_areas()

@router.post("/", response_model=AreaResponse)
def create_area(
    area_in: AreaCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([RoleEnum.admin]))
):
    """Cria uma nova área/cliente (Apenas Administrador)."""
    service = AreaService(db)
    return service.create_area(area_in)

@router.put("/{area_id}", response_model=AreaResponse)
def update_area(
    area_id: int,
    area_in: AreaUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([RoleEnum.admin]))
):
    """Atualiza o nome de uma área/cliente (Apenas Administrador)."""
    service = AreaService(db)
    return service.update_area(area_id, area_in)

@router.delete("/{area_id}")
def delete_area(
    area_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([RoleEnum.admin]))
):
    """Exclui uma área/cliente (Apenas Administrador)."""
    service = AreaService(db)
    service.delete_area(area_id)
    return {"message": "Área/Cliente excluída com sucesso."}

