from sqlalchemy.orm import Session
from app.models.area import Area
from app.schemas.area import AreaCreate, AreaUpdate

class AreaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Area).order_by(Area.name.asc()).all()

    def get_by_id(self, area_id: int):
        return self.db.query(Area).filter(Area.id == area_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Area).filter(Area.name == name).first()

    def create(self, area_in: AreaCreate):
        area = Area(name=area_in.name)
        self.db.add(area)
        self.db.commit()
        self.db.refresh(area)
        return area

    def update(self, area: Area, name: str):
        area.name = name
        self.db.commit()
        self.db.refresh(area)
        return area

    def delete(self, area: Area):
        self.db.delete(area)
        self.db.commit()
        return True

