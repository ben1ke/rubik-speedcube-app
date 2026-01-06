"""
Algorithm Service - Algoritmus CRUD műveletek.
OOP paradigma: Osztály alapú service layer.
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from backend.models.models import Algorithm
from backend.schemas.schemas import AlgorithmCreate

logger = logging.getLogger(__name__)


class AlgorithmService:
    """
    Algoritmusok kezelésére szolgáló service osztály.
    OOP paradigma: Osztály alapú architektúra üzleti logikával.
    """
    
    def __init__(self, db: Session):
        """
        Service inicializálása database session-nel.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def get_all(self, category: Optional[str] = None) -> List[Algorithm]:
        """
        Összes algoritmus lekérése, opcionális kategória szűréssel.
        
        Args:
            category: Opcionális kategória szűrő (pl. "PLL", "OLL")
        
        Returns:
            List[Algorithm]: Algoritmusok listája
        """
        try:
            query = self.db.query(Algorithm)
            
            if category:
                # Funkcionális elem: filter használata lambda-val
                query = query.filter(Algorithm.category == category)
            
            algorithms = query.order_by(Algorithm.name).all()
            logger.info(f"Retrieved {len(algorithms)} algorithms" + 
                       (f" for category {category}" if category else ""))
            return algorithms
        except Exception as e:
            logger.error(f"Error retrieving algorithms: {e}")
            raise
    
    def get_by_id(self, algorithm_id: int) -> Optional[Algorithm]:
        """
        Egy algoritmus lekérése ID alapján.
        
        Args:
            algorithm_id: Algoritmus azonosító
        
        Returns:
            Optional[Algorithm]: Algoritmus objektum vagy None
        """
        try:
            algorithm = self.db.query(Algorithm).filter(
                Algorithm.id == algorithm_id
            ).first()
            
            if algorithm:
                logger.info(f"Retrieved algorithm: {algorithm.name}")
            else:
                logger.warning(f"Algorithm not found with id: {algorithm_id}")
            
            return algorithm
        except Exception as e:
            logger.error(f"Error retrieving algorithm {algorithm_id}: {e}")
            raise
    
    def create(self, algorithm_data: AlgorithmCreate) -> Algorithm:
        """
        Új algoritmus létrehozása.
        
        Args:
            algorithm_data: Algoritmus adatok (Pydantic schema)
        
        Returns:
            Algorithm: Létrehozott algoritmus objektum
        
        Raises:
            ValueError: Ha az algoritmus név már létezik
        """
        try:
            # Ellenőrizzük, hogy létezik-e már ilyen nevű algoritmus
            existing = self.db.query(Algorithm).filter(
                Algorithm.name == algorithm_data.name
            ).first()
            
            if existing:
                raise ValueError(f"Algorithm with name '{algorithm_data.name}' already exists")
            
            # Új algoritmus létrehozása
            new_algorithm = Algorithm(
                name=algorithm_data.name,
                notation=algorithm_data.notation,
                category=algorithm_data.category,
                difficulty=algorithm_data.difficulty
            )
            
            self.db.add(new_algorithm)
            self.db.commit()
            self.db.refresh(new_algorithm)
            
            logger.info(f"Created new algorithm: {new_algorithm.name}")
            return new_algorithm
        except ValueError as ve:
            logger.warning(str(ve))
            raise
        except Exception as e:
            logger.error(f"Error creating algorithm: {e}")
            self.db.rollback()
            raise
    
    def delete(self, algorithm_id: int) -> bool:
        """
        Algoritmus törlése ID alapján.
        
        Args:
            algorithm_id: Törlendő algoritmus azonosító
        
        Returns:
            bool: True ha sikeres, False ha nem található
        """
        try:
            algorithm = self.db.query(Algorithm).filter(
                Algorithm.id == algorithm_id
            ).first()
            
            if not algorithm:
                logger.warning(f"Algorithm not found for deletion: {algorithm_id}")
                return False
            
            algorithm_name = algorithm.name
            self.db.delete(algorithm)
            self.db.commit()
            
            logger.info(f"Deleted algorithm: {algorithm_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting algorithm {algorithm_id}: {e}")
            self.db.rollback()
            raise
    
    def search(self, query: str) -> List[Algorithm]:
        """
        Algoritmusok keresése név alapján.
        Funkcionális paradigma: filter használata lambda kifejezéssel.
        
        Args:
            query: Keresési kifejezés
        
        Returns:
            List[Algorithm]: Talált algoritmusok listája
        """
        try:
            # SQL szintű keresés
            algorithms = self.db.query(Algorithm).filter(
                Algorithm.name.ilike(f"%{query}%")
            ).all()
            
            # Funkcionális paradigma: további szűrés lambda-val
            # Például csak azokat, amelyek neve tartalmazza a keresett szót
            filtered = list(filter(
                lambda alg: query.lower() in alg.name.lower() or 
                           query.lower() in alg.category.lower(),
                algorithms
            ))
            
            logger.info(f"Search for '{query}' returned {len(filtered)} results")
            return filtered
        except Exception as e:
            logger.error(f"Error searching algorithms: {e}")
            raise
    
    def get_by_category_grouped(self) -> dict:
        """
        Algoritmusok lekérése kategóriák szerint csoportosítva.
        Funkcionális paradigma: reduce-szerű csoportosítás.
        
        Returns:
            dict: Kategóriák szerint csoportosított algoritmusok
        """
        try:
            algorithms = self.db.query(Algorithm).order_by(Algorithm.category, Algorithm.name).all()
            
            # Funkcionális paradigma: csoportosítás
            grouped = {}
            for alg in algorithms:
                if alg.category not in grouped:
                    grouped[alg.category] = []
                grouped[alg.category].append(alg)
            
            logger.info(f"Grouped algorithms into {len(grouped)} categories")
            return grouped
        except Exception as e:
            logger.error(f"Error grouping algorithms: {e}")
            raise
