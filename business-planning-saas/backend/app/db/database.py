from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import settings

# Configuração do engine
if settings.ENVIRONMENT == "test":
    # Para testes, usar SQLite in-memory
    engine = create_engine(
        "sqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG
    )
else:
    # Para produção/desenvolvimento, usar PostgreSQL
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_recycle=300
    )

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()


def get_db():
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Remover todas as tabelas (usado em testes)"""
    Base.metadata.drop_all(bind=engine)