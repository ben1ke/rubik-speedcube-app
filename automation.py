"""
Automatizációs feladat - Napi scramble generálás
"""
import schedule
import time
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from models import SessionLocal, Scramble
from services import generate_scramble

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_daily_scramble():
    """
    Napi scramble automatikus generálása.
    Ez a függvény naponta fut és új scramble-t hoz létre.
    """
    logger.info("Starting daily scramble generation...")
    
    db: Session = SessionLocal()
    try:
        # Új scramble generálás
        new_scramble = generate_scramble(20)
        
        # Scramble mentése adatbázisba
        scramble = Scramble(
            scramble=new_scramble,
            used=0
        )
        db.add(scramble)
        db.commit()
        
        logger.info(f"Daily scramble generated: {new_scramble[:30]}...")
        
    except Exception as e:
        logger.error(f"Error generating daily scramble: {e}")
        db.rollback()
    finally:
        db.close()


def run_scheduler():
    """
    Scheduler futtatása.
    Minden nap 06:00-kor generál új scramble-t.
    """
    # Ütemezett feladat: minden nap 06:00
    schedule.every().day.at("06:00").do(generate_daily_scramble)
    
    logger.info("Scheduler started. Daily scramble at 06:00")
    logger.info("Press Ctrl+C to stop")
    
    # Első scramble generálás azonnal
    generate_daily_scramble()
    
    # Végtelen ciklus az ütemezett feladatok futtatásához
    while True:
        schedule.run_pending()
        time.sleep(60)  # Ellenőrzés percenként


if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
