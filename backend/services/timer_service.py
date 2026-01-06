"""
Timer Service - Scramble generálás és idő mentés.
Procedurális paradigma: Függvény alapú megközelítés.
"""
import random
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from backend.models.models import SolveTime, Scramble
from backend.schemas.schemas import SolveTimeCreate

logger = logging.getLogger(__name__)


# ============= PROCEDURÁLIS PARADIGMA =============
# Egyszerű függvények scramble generáláshoz


def generate_scramble(length: int = 20) -> str:
    """
    Random scramble (keverés) generálása procedurális módon.
    PROCEDURÁLIS PARADIGMA: Egyszerű függvény, ciklusok, feltételek.
    
    Args:
        length: Scramble lépéseinek száma (alapértelmezett: 20)
    
    Returns:
        str: Generált scramble notációban (pl. "R U R' U' F2 D...")
    """
    moves = ["R", "L", "U", "D", "F", "B"]
    modifiers = ["", "'", "2"]
    
    scramble_sequence = []
    last_move = None
    
    for _ in range(length):
        # Válasszunk egy lépést, ami nem egyezik az előzővel
        move = random.choice(moves)
        
        # Kerüljük az ismétlődést (pl. "R R'" helyett)
        while move == last_move:
            move = random.choice(moves)
        
        modifier = random.choice(modifiers)
        scramble_sequence.append(move + modifier)
        last_move = move
    
    result = " ".join(scramble_sequence)
    logger.info(f"Generated scramble: {result[:50]}...")
    return result


def validate_time(time_value: float) -> bool:
    """
    Idő validálása procedurális módon.
    PROCEDURÁLIS PARADIGMA: Egyszerű ellenőrzési logika.
    
    Args:
        time_value: Ellenőrizendő idő (másodpercben)
    
    Returns:
        bool: True ha érvényes, False különben
    """
    # Alapvető validációk
    if time_value <= 0:
        logger.warning(f"Invalid time value: {time_value} (must be positive)")
        return False
    
    if time_value > 3600:  # 1 óra (valószínűleg hiba)
        logger.warning(f"Suspicious time value: {time_value} (over 1 hour)")
        return False
    
    return True


def format_time(seconds: float) -> str:
    """
    Idő formázása olvasható formátumra.
    PROCEDURÁLIS PARADIGMA: String műveletekkel.
    
    Args:
        seconds: Másodpercek (float)
    
    Returns:
        str: Formázott idő (pl. "12.34" vagy "1:23.45")
    """
    if seconds < 60:
        return f"{seconds:.2f}"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}:{secs:05.2f}"


# ============= SERVICE OSZTÁLY =============


class TimerService:
    """
    Timer service osztály idő mentéshez és lekéréshez.
    OOP paradigma: Osztály alapú architektúra.
    """
    
    def __init__(self, db: Session):
        """
        Service inicializálása database session-nel.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def save_time(self, time_data: SolveTimeCreate) -> SolveTime:
        """
        Kirakási idő mentése az adatbázisba.
        
        Args:
            time_data: Idő adatok (Pydantic schema)
        
        Returns:
            SolveTime: Mentett idő objektum
        
        Raises:
            ValueError: Ha az idő érvénytelen
        """
        try:
            # Procedurális validáció használata
            if not validate_time(time_data.time):
                raise ValueError(f"Invalid time value: {time_data.time}")
            
            # Új solve time létrehozása
            new_time = SolveTime(
                time=time_data.time,
                scramble=time_data.scramble,
                dnf=time_data.dnf
            )
            
            self.db.add(new_time)
            self.db.commit()
            self.db.refresh(new_time)
            
            status = "DNF" if new_time.dnf else format_time(new_time.time)
            logger.info(f"Saved solve time: {status}")
            return new_time
        except ValueError as ve:
            logger.warning(str(ve))
            raise
        except Exception as e:
            logger.error(f"Error saving solve time: {e}")
            self.db.rollback()
            raise
    
    def get_all_times(self, limit: Optional[int] = None) -> List[SolveTime]:
        """
        Összes kirakási idő lekérése.
        
        Args:
            limit: Maximális visszaadott elemek száma (None = összes)
        
        Returns:
            List[SolveTime]: Kirakási idők listája (legújabb először)
        """
        try:
            query = self.db.query(SolveTime).order_by(SolveTime.date.desc())
            
            if limit:
                query = query.limit(limit)
            
            times = query.all()
            logger.info(f"Retrieved {len(times)} solve times")
            return times
        except Exception as e:
            logger.error(f"Error retrieving solve times: {e}")
            raise
    
    def get_by_id(self, time_id: int) -> Optional[SolveTime]:
        """
        Egy kirakási idő lekérése ID alapján.
        
        Args:
            time_id: Idő azonosító
        
        Returns:
            Optional[SolveTime]: Idő objektum vagy None
        """
        try:
            solve_time = self.db.query(SolveTime).filter(
                SolveTime.id == time_id
            ).first()
            
            if solve_time:
                logger.info(f"Retrieved solve time: {solve_time.id}")
            else:
                logger.warning(f"Solve time not found with id: {time_id}")
            
            return solve_time
        except Exception as e:
            logger.error(f"Error retrieving solve time {time_id}: {e}")
            raise
    
    def get_recent(self, limit: int = 10) -> List[SolveTime]:
        """
        Legutóbbi N kirakási idő lekérése.
        
        Args:
            limit: Visszaadott elemek száma (alapértelmezett: 10)
        
        Returns:
            List[SolveTime]: Legutóbbi idők listája
        """
        return self.get_all_times(limit=limit)
    
    def generate_and_save_scramble(self) -> Scramble:
        """
        Új scramble generálása és mentése az adatbázisba.
        Procedurális scramble generálás használata.
        
        Returns:
            Scramble: Mentett scramble objektum
        """
        try:
            # Procedurális függvény használata
            scramble_text = generate_scramble()
            
            # Ellenőrizzük, hogy létezik-e már
            existing = self.db.query(Scramble).filter(
                Scramble.scramble == scramble_text
            ).first()
            
            if existing:
                # Ha már létezik, generáljunk újat (rekurzív hívás)
                logger.info("Scramble already exists, generating new one")
                return self.generate_and_save_scramble()
            
            # Új scramble mentése
            new_scramble = Scramble(
                scramble=scramble_text,
                used=0
            )
            
            self.db.add(new_scramble)
            self.db.commit()
            self.db.refresh(new_scramble)
            
            logger.info(f"Saved new scramble: {scramble_text[:50]}...")
            return new_scramble
        except Exception as e:
            logger.error(f"Error generating scramble: {e}")
            self.db.rollback()
            raise
    
    def get_daily_scramble(self) -> str:
        """
        Napi scramble lekérése vagy generálása.
        Ha már volt ma scramble, azt adja vissza, különben újat generál.
        
        Returns:
            str: Napi scramble szövege
        """
        try:
            today = datetime.now().date()
            
            # Keressük meg a mai napra generált scramble-t
            today_scramble = self.db.query(Scramble).filter(
                Scramble.date >= datetime.combine(today, datetime.min.time())
            ).first()
            
            if today_scramble:
                logger.info("Retrieved today's scramble from database")
                return today_scramble.scramble
            else:
                # Generáljunk újat
                logger.info("Generating new daily scramble")
                new_scramble = self.generate_and_save_scramble()
                return new_scramble.scramble
        except Exception as e:
            logger.error(f"Error getting daily scramble: {e}")
            # Fallback: generáljunk egy scramble-t anélkül, hogy mentenénk
            return generate_scramble()
    
    def mark_scramble_used(self, scramble_id: int) -> bool:
        """
        Scramble megjelölése használtként.
        
        Args:
            scramble_id: Scramble azonosító
        
        Returns:
            bool: True ha sikeres
        """
        try:
            scramble = self.db.query(Scramble).filter(
                Scramble.id == scramble_id
            ).first()
            
            if scramble:
                scramble.used = 1
                self.db.commit()
                logger.info(f"Marked scramble {scramble_id} as used")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error marking scramble as used: {e}")
            self.db.rollback()
            raise
