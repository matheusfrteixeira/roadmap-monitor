from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    gestor = "gestor"
    analista = "analista"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.analista, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    manager = relationship("User", remote_side=[id], backref="subordinates")
