from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.activity_repo import ActivityRepository
from app.repositories.time_entry_repo import TimeEntryRepository
from app.services.project_service import ProjectService
from app.services.deliverable_service import DeliverableService
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.models.activity import Activity
from app.models.user import User

class ActivityService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ActivityRepository(db)
        self.time_entry_repo = TimeEntryRepository(db)
        self.project_service = ProjectService(db)
        self.deliverable_service = DeliverableService(db)

    def _enrich_activity(self, activity: Activity):
        activity.assignee_name = activity.assignee.name if activity.assignee else None
        activity.deliverable_name = activity.deliverable.name if activity.deliverable else None
        
        today = date.today()
        activity.is_delayed = bool(
            activity.status != 'Concluído' and (activity.progress is None or activity.progress < 100) and activity.end_date and activity.end_date < today
        )
        
        minutes = self.time_entry_repo.get_total_minutes_by_activity(activity.id)
        activity.total_tracked_minutes = minutes
        activity.total_tracked_hours = round(minutes / 60.0, 1)
        return activity

    def get_all_activities(self):
        activities = self.repo.get_all()
        return [self._enrich_activity(a) for a in activities]

    def create_activity(self, activity_in: ActivityCreate):
        project = self.project_service.get_project_by_id(activity_in.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projeto pai não encontrado.")

        activity_obj = Activity(**activity_in.model_dump())
        created = self.repo.create(activity_obj)

        # Recalcula métricas do entregável se houver
        if created.deliverable_id:
            self.deliverable_service.recalculate_deliverable_metrics(created.deliverable_id)

        # Recalcula datas e progresso do projeto pai automaticamente
        self.project_service.recalculate_project_metrics(activity_in.project_id)

        return self._enrich_activity(created)

    def update_activity(self, activity_id: int, activity_in: ActivityUpdate, current_user: User):
        activity = self.repo.get_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Atividade não encontrada.")
        
        old_deliverable_id = activity.deliverable_id
        update_data = activity_in.model_dump(exclude_unset=True)
        updated = self.repo.update(activity, update_data)

        # Recalcula entregáveis afetados
        if old_deliverable_id:
            self.deliverable_service.recalculate_deliverable_metrics(old_deliverable_id)
        if updated.deliverable_id and updated.deliverable_id != old_deliverable_id:
            self.deliverable_service.recalculate_deliverable_metrics(updated.deliverable_id)

        # Recalcula datas e progresso do projeto pai automaticamente
        self.project_service.recalculate_project_metrics(activity.project_id)

        return self._enrich_activity(updated)

    def delete_activity(self, activity_id: int, current_user: User):
        activity = self.repo.get_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Atividade não encontrada.")
        
        project_id = activity.project_id
        deliverable_id = activity.deliverable_id

        self.db.delete(activity)
        self.db.commit()

        if deliverable_id:
            self.deliverable_service.recalculate_deliverable_metrics(deliverable_id)

        # Recalcula métricas do projeto pai
        self.project_service.recalculate_project_metrics(project_id)
        return True
