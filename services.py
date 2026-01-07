"""
Service logika - 3 PROGRAMOZÁSI PARADIGMA DEMONSTRÁCIÓJA
"""
import random
from typing import List, Optional
from functools import reduce
from sqlalchemy.orm import Session
from models import SolveTime, Scramble
import logging

logger = logging.getLogger(__name__)


# ============================================
# PROCEDURÁLIS PARADIGMA
# ============================================
def generate_scramble(length: int = 20) -> str:
    """
    Procedurális scramble generálás.
    Lépésről lépésre végrehajtás, egyszerű for ciklus.
    """
    moves = ["R", "L", "U", "D", "F", "B"]
    modifiers = ["", "'", "2"]
    scramble = []
    
    for _ in range(length):
        move = random.choice(moves)
        modifier = random.choice(modifiers)
        scramble.append(f"{move}{modifier}")
    
    result = " ".join(scramble)
    logger.info(f"Generated scramble: {result[:50]}...")
    return result


def format_time(seconds: float) -> str:
    """
    Procedurális időformázás.
    Szekvenciális lépések, if-else.
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:05.2f}"


# ============================================
# FUNKCIONÁLIS PARADIGMA
# ============================================
def calculate_average(times: List[float]) -> Optional[float]:
    """
    Funkcionális átlagszámítás reduce-sal.
    Higher-order function, immutable adatok.
    """
    if not times:
        return None
    total = reduce(lambda acc, x: acc + x, times, 0.0)
    return total / len(times)


def get_best_time(times: List[float]) -> Optional[float]:
    """
    Funkcionális minimum keresés.
    Built-in higher-order function (min).
    """
    return min(times) if times else None


def filter_recent_times(all_times: List[SolveTime], limit: int = 5) -> List[float]:
    """
    Funkcionális filter + map kombináció.
    Lambda expressions használata.
    """
    recent = sorted(all_times, key=lambda t: t.date, reverse=True)[:limit]
    return list(map(lambda t: t.time, recent))


# ============================================
# OBJEKTUM-ORIENTÁLT PARADIGMA
# ============================================
class TimerService:
    """
    OOP service osztály.
    Encapsulation, methods, dependency injection.
    """
    
    def __init__(self, db: Session):
        """Constructor - dependency injection."""
        self.db = db
        logger.info("TimerService initialized")
    
    def save_time(self, time: float, scramble: str) -> SolveTime:
        """Idő mentése adatbázisba."""
        solve = SolveTime(time=time, scramble=scramble)
        self.db.add(solve)
        self.db.commit()
        self.db.refresh(solve)
        logger.info(f"Saved solve time: {time}s")
        return solve
    
    def get_all_times(self) -> List[SolveTime]:
        """Összes idő lekérdezése."""
        return self.db.query(SolveTime).order_by(SolveTime.date.desc()).all()
    
    def get_statistics(self) -> dict:
        """
        Statisztikák számítása.
        OOP method + funkcionális elemek kombinálása.
        """
        times = self.get_all_times()
        time_values = [t.time for t in times]
        
        return {
            "total_solves": len(times),
            "best_time": get_best_time(time_values),
            "average": calculate_average(time_values),
            "last_5_avg": calculate_average(filter_recent_times(times, 5))
        }


class ScrambleService:
    """OOP scramble service."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_daily_scramble(self) -> str:
        """Napi scramble lekérése vagy generálása."""
        scramble = self.db.query(Scramble).filter(Scramble.used == 0).first()
        
        if not scramble:
            scramble_text = generate_scramble()
            scramble = Scramble(scramble=scramble_text, used=0)
            self.db.add(scramble)
            self.db.commit()
            self.db.refresh(scramble)
        
        return scramble.scramble
    
    def mark_used(self, scramble_id: int):
        """Scramble használt jelölése."""
        scramble = self.db.query(Scramble).filter(Scramble.id == scramble_id).first()
        if scramble:
            scramble.used = 1
            self.db.commit()
