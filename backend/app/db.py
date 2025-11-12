from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

# Construimos la URL de conexión a MySQL con PyMySQL (driver puro Python)
DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Engine de SQLAlchemy: maneja conexiones, pooling, etc.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Verifica conexión antes de usarla (evita conexiones zombi)
    pool_recycle=3600,    # Recicla conexiones cada X segundos (MySQL cierra inactivas)
    future=True,          # API 2.0 de SQLAlchemy
)

# Factoría de sesiones: cada request usará una sesión independiente (scoped por dependencia)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

# Base declarativa: de aquí heredan nuestros modelos ORM
class Base(DeclarativeBase):
    pass

# Dependencia para FastAPI: abre/cierra sesión por petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
