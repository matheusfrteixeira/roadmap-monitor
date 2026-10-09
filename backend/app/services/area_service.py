from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.area_repo import AreaRepository
from app.schemas.area import AreaCreate, AreaUpdate

class AreaService:
    def __init__(self, db: Session):
        self.repo = AreaRepository(db)

    def get_all_areas(self):
        return self.repo.get_all()

    def create_area(self, area_in: AreaCreate):
        existing = self.repo.get_by_name(area_in.name)
        if existing:
            raise HTTPException(status_code=400, detail="Esta Área/Cliente já está cadastrada.")
        return self.repo.create(area_in)

    def update_area(self, area_id: int, area_in: AreaUpdate):
        area = self.repo.get_by_id(area_id)
        if not area:
            raise HTTPException(status_code=404, detail="Área/Cliente não encontrada.")
        return self.repo.update(area, area_in.name)

    def delete_area(self, area_id: int):
        area = self.repo.get_by_id(area_id)
        if not area:
            raise HTTPException(status_code=404, detail="Área/Cliente não encontrada.")
        return self.repo.delete(area)

