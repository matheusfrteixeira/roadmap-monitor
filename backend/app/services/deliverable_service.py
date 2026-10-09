from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.deliverable_repo import DeliverableRepository
from app.repositories.time_entry_repo import TimeEntryRepository
from app.schemas.deliverable import DeliverableCreate, DeliverableUpdate
from app.models.deliverable import Deliverable
from app.models.project import Project

class DeliverableService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = DeliverableRepository(db)
        self.time_entry_repo = TimeEntryRepository(db)

    def _enrich_deliverable(self, deliverable: Deliverable):
        activities = deliverable.activities or []
        deliverable.total_activities = len(activities)
        deliverable.completed_activities = len([
            a for a in activities if a.status == 'Concluído' or (a.progress and a.progress >= 100)
        ])
        today = date.today()
        deliverable.delayed_activities = len([
            a for a in activities
            if a.status != 'Concluído' and (a.progress is None or a.progress < 100) and a.end_date and a.end_date < today
        ])
        minutes = self.time_entry_repo.get_total_minutes_by_deliverable(deliverable.id)
        deliverable.total_tracked_minutes = minutes
        deliverable.total_tracked_hours = round(minutes / 60.0, 1)
        return deliverable

    def get_all(self):
        items = self.repo.get_all()
        return [self._enrich_deliverable(d) for d in items]

    def get_by_project(self, project_id: int):
        items = self.repo.get_by_project(project_id)
        return [self._enrich_deliverable(d) for d in items]

    def get_by_id(self, deliverable_id: int):
        item = self.repo.get_by_id(deliverable_id)
        if not item:
            return None
        return self._enrich_deliverable(item)

    def create_deliverable(self, deliverable_in: DeliverableCreate):
        project = self.db.query(Project).filter(Project.id == deliverable_in.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Projeto pai não encontrado.")

        obj = Deliverable(**deliverable_in.model_dump())
        created = self.repo.create(obj)
        return self._enrich_deliverable(created)

    def update_deliverable(self, deliverable_id: int, deliverable_in: DeliverableUpdate):
        item = self.repo.get_by_id(deliverable_id)
        if not item:
            raise HTTPException(status_code=404, detail="Entregável não encontrado.")

        update_data = deliverable_in.model_dump(exclude_unset=True)
        updated = self.repo.update(item, update_data)
        return self._enrich_deliverable(updated)

    def delete_deliverable(self, deliverable_id: int):
        item = self.repo.get_by_id(deliverable_id)
        if not item:
            raise HTTPException(status_code=404, detail="Entregável não encontrado.")

        project_id = item.project_id
        self.repo.delete(item)

        # Recalcula métricas do projeto após exclusão
        from app.services.project_service import ProjectService
        ProjectService(self.db).recalculate_project_metrics(project_id)
        return True

    def recalculate_deliverable_metrics(self, deliverable_id: int):
        deliverable = self.repo.get_by_id(deliverable_id)
        if not deliverable:
            return None

        activities = deliverable.activities or []
        if activities:
            valid_starts = [a.start_date for a in activities if a.start_date]
            valid_ends = [a.end_date for a in activities if a.end_date]

            if valid_starts:
                deliverable.start_date = min(valid_starts)
            if valid_ends:
                deliverable.end_date = max(valid_ends)

            tot = len(activities)
            concl = len([a for a in activities if a.status == 'Concluído' or (a.progress and a.progress >= 100)])
            deliverable.progress = round((concl / tot) * 100, 1)

            if deliverable.progress >= 100:
                deliverable.status = "Concluído"
            elif deliverable.progress > 0:
                deliverable.status = "Em Andamento"

            self.db.commit()
            self.db.refresh(deliverable)

        return self._enrich_deliverable(deliverable)

