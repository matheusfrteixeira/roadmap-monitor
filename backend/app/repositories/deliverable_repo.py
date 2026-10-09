from sqlalchemy.orm import Session
from app.models.deliverable import Deliverable

class DeliverableRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Deliverable).all()

    def get_by_id(self, deliverable_id: int):
        return self.db.query(Deliverable).filter(Deliverable.id == deliverable_id).first()

    def get_by_project(self, project_id: int):
        return self.db.query(Deliverable).filter(Deliverable.project_id == project_id).all()

    def create(self, deliverable_obj: Deliverable):
        self.db.add(deliverable_obj)
        self.db.commit()
        self.db.refresh(deliverable_obj)
        return deliverable_obj

    def update(self, deliverable: Deliverable, update_data: dict):
        for field, value in update_data.items():
            setattr(deliverable, field, value)
        self.db.commit()
        self.db.refresh(deliverable)
        return deliverable

    def delete(self, deliverable: Deliverable):
        self.db.delete(deliverable)
        self.db.commit()

