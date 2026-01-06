"""
SQLAlchemy adatbázis kapcsolat és session kezelés.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

from backend.config import get_settings

# Logging beállítása
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Beállítások betöltése
settings = get_settings()

# SQLAlchemy engine létrehozása
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # SQLite-hoz szükséges
    echo=False  # SQL query logging (fejlesztéshez True-ra állítható)
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Deklaratív base osztály minden modellhez
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection függvény FastAPI-hoz.
    Biztosítja, hogy minden request után bezáródik a session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        logger.info("Database session created")
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.info("Database session closed")


def init_db() -> None:
    """
    Adatbázis inicializálása - táblák létrehozása.
    """
    try:
        # Importáljuk a modelleket hogy a Base.metadata ismerje őket
        from backend.models import models
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise
