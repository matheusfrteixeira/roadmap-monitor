from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def _enrich_user(self, user: User):
        user.manager_name = user.manager.name if user.manager else None
        return user

    def get_user_by_email(self, email: str):
        user = self.repo.get_by_email(email)
        return self._enrich_user(user) if user else None

    def get_all_users(self):
        users = self.repo.get_all()
        return [self._enrich_user(u) for u in users]

    def create_user(self, user_in: UserCreate):
        if self.repo.get_by_email(user_in.email):
            raise HTTPException(status_code=400, detail="O email já está registrado.")
        
        user_obj = User(
            email=user_in.email,
            name=user_in.name,
            role=user_in.role,
            manager_id=user_in.manager_id,
            hashed_password=get_password_hash(user_in.password),
        )
        created = self.repo.create(user_obj)
        return self._enrich_user(created)

    def update_user(self, user_id: int, user_in: UserUpdate):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        elif "password" in update_data:
            update_data.pop("password")

        updated = self.repo.update(user, update_data)
        return self._enrich_user(updated)
