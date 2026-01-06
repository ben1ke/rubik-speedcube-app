"""
SQLAlchemy ORM modellek az adatbázis táblákhoz.
3 fő entitás: Algorithm, SolveTime, Scramble
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime

from backend.database import Base


class Algorithm(Base):
    """
    Rubik kocka algoritmusok tárolása.
    
    Attributes:
        id: Elsődleges kulcs
        name: Algoritmus neve (pl. "T-Perm")
        notation: Lépéssorozat notációban (pl. "R U R' U'...")
        category: Kategória (PLL, OLL, F2L, stb.)
        difficulty: Nehézségi szint (Kezdő, Haladó, Expert)
        created_at: Létrehozás időpontja
    """
    __tablename__ = "algorithms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    notation = Column(String(500), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(20), nullable=False, default="Kezdő")
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<Algorithm(name='{self.name}', category='{self.category}')>"


class SolveTime(Base):
    """
    Kirakási idők tárolása.
    
    Attributes:
        id: Elsődleges kulcs
        time: Kirakási idő másodpercben
        scramble: Használt keverés
        date: Kirakás időpontja
        dnf: Did Not Finish jelző (0=sikeres, 1=DNF)
    """
    __tablename__ = "solve_times"
    
    id = Column(Integer, primary_key=True, index=True)
    time = Column(Float, nullable=False)
    scramble = Column(String(500), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, server_default=func.now(), index=True)
    dnf = Column(Integer, default=0, nullable=False)  # 0=sikeres, 1=DNF
    
    def __repr__(self) -> str:
        dnf_status = "DNF" if self.dnf else f"{self.time}s"
        return f"<SolveTime(time='{dnf_status}', date='{self.date}')>"


class Scramble(Base):
    """
    Generált keverések tárolása.
    
    Attributes:
        id: Elsődleges kulcs
        scramble: Keverés notációban
        date: Generálás időpontja
        used: Felhasználva volt-e már (0=nem, 1=igen)
    """
    __tablename__ = "scrambles"
    
    id = Column(Integer, primary_key=True, index=True)
    scramble = Column(String(500), nullable=False, unique=True)
    date = Column(DateTime, default=datetime.utcnow, server_default=func.now(), index=True)
    used = Column(Integer, default=0, nullable=False)  # 0=nem használt, 1=használt
    
    def __repr__(self) -> str:
        status = "used" if self.used else "unused"
        return f"<Scramble(scramble='{self.scramble[:20]}...', status='{status}')>"
