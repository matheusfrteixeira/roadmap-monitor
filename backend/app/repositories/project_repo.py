from sqlalchemy.orm import Session
from app.models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Project).all()

    def get_by_id(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id).first()

    def create(self, project_obj: Project):
        self.db.add(project_obj)
        self.db.commit()
        self.db.refresh(project_obj)
        return project_obj

    def update(self, project: Project, update_data: dict):
        for field, value in update_data.items():
            setattr(project, field, value)
        self.db.commit()
        self.db.refresh(project)
        return project

