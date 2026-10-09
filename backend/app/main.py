from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Garante que todos os modelos SQLAlchemy e listeners sejam carregados na inicialização
import app.models
import app.db.audit

from app.api.routes import auth, users, projects, deliverables, activities, timetracker, areas

app = FastAPI(
    title="RoadMap Corporate Monitor API",
    description="API de Controle de Demandas, Projetos e Timetracker",
    version="1.0.0"
)

# Configurando CORS para o Frontend Vue3 conversar com o Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção alterar para ["http://localhost:5173"] do Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do RoadMap Corporate Monitor!"}

# Incluindo Rotas (Routers)
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/api/users", tags=["Usuários"])
app.include_router(areas.router, prefix="/api/areas", tags=["Áreas/Clientes"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projetos"])
app.include_router(deliverables.router, prefix="/api/deliverables", tags=["Entregáveis"])
app.include_router(activities.router, prefix="/api/activities", tags=["Atividades"])
app.include_router(timetracker.router, prefix="/api/timetracker", tags=["Timetracker"])
