from sqlalchemy.orm import Session
from app.models.activity import Activity

class ActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Activity).all()

    def get_by_id(self, activity_id: int):
        return self.db.query(Activity).filter(Activity.id == activity_id).first()

    def create(self, activity_obj: Activity):
        self.db.add(activity_obj)
        self.db.commit()
        self.db.refresh(activity_obj)
        return activity_obj

    def update(self, activity: Activity, update_data: dict):
        for field, value in update_data.items():
            setattr(activity, field, value)
        self.db.commit()
        self.db.refresh(activity)
        return activity

