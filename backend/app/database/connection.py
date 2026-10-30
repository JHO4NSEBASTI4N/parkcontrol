from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Configuracion

motor = create_engine(
    Configuracion.database_url,
    pool_pre_ping=True
    )

SessionLocal = sessionmaker(
    bind=motor,
    autocommit=False,
    autoflush=False
)

def obtener_sesion():
    sesion = SessionLocal()
    try:
        yield sesion
    finally:
        sesion.close()