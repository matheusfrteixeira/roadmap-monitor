from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.time_entry import TimeEntry
from app.models.active_timer import ActiveTimer
from app.models.activity import Activity

class TimeEntryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int):
        return self.db.query(TimeEntry).filter(TimeEntry.user_id == user_id).order_by(TimeEntry.date_recorded.desc()).all()

    def get_by_activity_id(self, activity_id: int):
        return self.db.query(TimeEntry).filter(TimeEntry.activity_id == activity_id).order_by(TimeEntry.date_recorded.desc()).all()

    def get_by_project_id(self, project_id: int):
        return self.db.query(TimeEntry)\
            .join(Activity, TimeEntry.activity_id == Activity.id)\
            .filter(Activity.project_id == project_id)\
            .order_by(TimeEntry.date_recorded.desc())\
            .all()

    def get_total_minutes_by_activity(self, activity_id: int):
        total = self.db.query(func.sum(TimeEntry.time_spent_minutes))\
            .filter(TimeEntry.activity_id == activity_id)\
            .scalar()
        return int(total or 0)

    def get_total_minutes_by_deliverable(self, deliverable_id: int):
        total = self.db.query(func.sum(TimeEntry.time_spent_minutes))\
            .join(Activity, TimeEntry.activity_id == Activity.id)\
            .filter(Activity.deliverable_id == deliverable_id)\
            .scalar()
        return int(total or 0)

    def get_total_minutes_by_project(self, project_id: int):
        total = self.db.query(func.sum(TimeEntry.time_spent_minutes))\
            .join(Activity, TimeEntry.activity_id == Activity.id)\
            .filter(Activity.project_id == project_id)\
            .scalar()
        return int(total or 0)

    def create(self, entry_obj: TimeEntry):
        self.db.add(entry_obj)
        self.db.commit()
        self.db.refresh(entry_obj)
        return entry_obj

    def get_active_timer_by_user(self, user_id: int):
        return self.db.query(ActiveTimer).filter(ActiveTimer.user_id == user_id).first()

    def create_active_timer(self, active_timer_obj: ActiveTimer):
        self.db.add(active_timer_obj)
        self.db.commit()
        self.db.refresh(active_timer_obj)
        return active_timer_obj

    def delete_active_timer(self, active_timer_obj: ActiveTimer):
        self.db.delete(active_timer_obj)
        self.db.commit()
