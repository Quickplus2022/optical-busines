from sqlmodel import create_engine, Session

from .config import settings

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    """Dependency que fornece uma sessão do banco de dados."""
    with Session(engine) as session:
        yield session