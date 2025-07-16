from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Configurações globais carregadas de variáveis de ambiente (.env)."""

    project_name: str = "BizPlanner SaaS"

    # Banco de dados PostgreSQL
    postgres_user: str = Field("postgres", env="POSTGRES_USER")
    postgres_password: str = Field("postgres", env="POSTGRES_PASSWORD")
    postgres_db: str = Field("bizplanner", env="POSTGRES_DB")
    postgres_host: str = Field("db", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()