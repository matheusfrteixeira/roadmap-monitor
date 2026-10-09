from app.db.session import SessionLocal
from app.models.user import User, RoleEnum
from app.core.security import get_password_hash

db = SessionLocal()
try:
    user = db.query(User).filter(User.email == "admin@roadmap.com").first()
    if not user:
        admin_user = User(
            name="Administrador do Sistema",
            email="admin@roadmap.com",
            hashed_password=get_password_hash("admin123"),
            role=RoleEnum.admin
        )
        db.add(admin_user)
        db.commit()
        print("Usuário administrador criado com sucesso!")
        print("Email: admin@roadmap.com | Senha: admin123")
    else:
        print("Usuário administrador já existe no banco de dados.")
except Exception as e:
    print(f"Erro ao criar admin: {e}")
finally:
    db.close()

