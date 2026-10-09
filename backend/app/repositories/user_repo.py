from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self):
        return self.db.query(User).order_by(User.name.asc()).all()

    def create(self, user_obj: User):
        self.db.add(user_obj)
        self.db.commit()
        self.db.refresh(user_obj)
        return user_obj

    def update(self, user: User, update_data: dict):
        for field, value in update_data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user
