from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.project_repo import ProjectRepository
from app.repositories.time_entry_repo import TimeEntryRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.project import Project

class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProjectRepository(db)
        self.time_entry_repo = TimeEntryRepository(db)

    def _enrich_project(self, project: Project):
        total = len(project.activities) if project.activities else 0
        completed = len([a for a in project.activities if a.status == 'Concluído' or (a.progress and a.progress >= 100)]) if project.activities else 0
        project.total_deliverables = len(project.deliverables) if project.deliverables else 0
        project.total_activities = total
        project.completed_activities = completed
        
        today = date.today()
        delayed_count = len([
            a for a in project.activities
            if a.status != 'Concluído' and (a.progress is None or a.progress < 100) and a.end_date and a.end_date < today
        ]) if project.activities else 0
        project.delayed_activities = delayed_count

        project.area_name = project.area.name if project.area else None
        project.owner_name = project.owner.name if project.owner else None
        project.manager_name = project.owner.manager.name if project.owner and project.owner.manager else None
        project.manager_id = project.owner.manager_id if project.owner else None
        
        minutes = self.time_entry_repo.get_total_minutes_by_project(project.id)
        project.total_tracked_minutes = minutes
        project.total_tracked_hours = round(minutes / 60.0, 1)
        return project

    def get_all_projects(self):
        projects = self.repo.get_all()
        return [self._enrich_project(p) for p in projects]
        
    def get_project_by_id(self, project_id: int):
        project = self.repo.get_by_id(project_id)
        if not project:
            return None
        return self._enrich_project(project)

    def create_project(self, project_in: ProjectCreate):
        project_obj = Project(**project_in.model_dump())
        created = self.repo.create(project_obj)
        return self._enrich_project(created)

    def update_project(self, project_id: int, project_in: ProjectUpdate):
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projeto não encontrado.")
        
        update_data = project_in.model_dump(exclude_unset=True)
        updated = self.repo.update(project, update_data)
        return self._enrich_project(updated)

    def recalculate_project_metrics(self, project_id: int):
        """Recalcula início, término e progresso do projeto com base nas atividades."""
        project = self.repo.get_by_id(project_id)
        if not project:
            return None

        activities = project.activities
        if activities:
            valid_starts = [a.start_date for a in activities if a.start_date]
            valid_ends = [a.end_date for a in activities if a.end_date]

            if valid_starts:
                project.start_date = min(valid_starts)
            if valid_ends:
                project.end_date = max(valid_ends)

            total = len(activities)
            completed = len([a for a in activities if a.status == 'Concluído' or (a.progress and a.progress >= 100)])
            project.progress = round((completed / total) * 100, 1)

            self.db.commit()
            self.db.refresh(project)

        return self._enrich_project(project)
