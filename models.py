"""
ORM modellek SQLAlchemy-val - OBJEKTUM-ORIENTÁLT PARADIGMA
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
import os

# SQLAlchemy Base
Base = declarative_base()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./speedcube.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Adatbázis táblák létrehozása."""
    Base.metadata.create_all(bind=engine)


# ORM Modellek
class SolveTime(Base):
    """Solve time ORM modell."""
    __tablename__ = "solve_times"
    
    id = Column(Integer, primary_key=True, index=True)
    time = Column(Float, nullable=False)
    scramble = Column(String(500), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


class Scramble(Base):
    """Scramble ORM modell."""
    __tablename__ = "scrambles"
    
    id = Column(Integer, primary_key=True, index=True)
    scramble = Column(String(500), nullable=False, unique=True)
    date = Column(DateTime, default=datetime.utcnow)
    used = Column(Integer, default=0)


# Pydantic sémák
class SolveTimeCreate(BaseModel):
    """Solve time létrehozási séma."""
    time: float = Field(..., description="Idő másodpercben")
    scramble: str = Field(..., min_length=1, max_length=500)


class SolveTimeResponse(BaseModel):
    """Solve time response séma."""
    id: int
    time: float
    scramble: str
    date: datetime
    
    class Config:
        from_attributes = True


class ScrambleResponse(BaseModel):
    """Scramble response séma."""
    id: int
    scramble: str
    date: datetime
    used: int
    
    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    """Statisztika response séma."""
    total_solves: int
    best_time: Optional[float]
    average: Optional[float]
    last_5_avg: Optional[float]
