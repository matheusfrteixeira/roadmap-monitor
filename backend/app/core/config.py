from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RoadMap Corporate Monitor"
    # Substituir no ambiente de produção
    DATABASE_URL: str = "mysql+pymysql://root:password@127.0.0.1/roadmap"
    SECRET_KEY: str = "sua_chave_secreta_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"

settings = Settings()

