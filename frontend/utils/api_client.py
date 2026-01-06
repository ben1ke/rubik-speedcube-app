"""
API Client - Backend API hívások wrapper osztálya.
Központosított HTTP kommunikáció a FastAPI backend-del.
"""
import requests
from typing import Optional, List, Dict, Any
import logging
import os

# Logging beállítása
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend URL environment változóból vagy alapértelmezett
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


class APIClient:
    """
    API Client osztály a backend kommunikációhoz.
    OOP paradigma: Osztály alapú API wrapper.
    """
    
    def __init__(self, base_url: str = BACKEND_URL):
        """
        API Client inicializálása.
        
        Args:
            base_url: Backend API alap URL
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        logger.info(f"API Client initialized with base URL: {base_url}")
    
    def _handle_response(self, response: requests.Response) -> Any:
        """
        HTTP válasz kezelése és hibakezelés.
        
        Args:
            response: requests Response objektum
        
        Returns:
            Any: Parse-olt JSON válasz
        
        Raises:
            Exception: HTTP hiba esetén
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            logger.error(f"Response: {response.text}")
            raise
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            raise
    
    # ============= SCRAMBLE METHODS =============
    
    def get_scramble(self) -> Dict[str, Any]:
        """
        Random scramble generálása.
        
        Returns:
            Dict: Scramble adatok
        """
        try:
            response = requests.get(f"{self.api_url}/scramble")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting scramble: {e}")
            return {"scramble": "Error generating scramble", "length": 0}
    
    def get_daily_scramble(self) -> Dict[str, Any]:
        """
        Napi scramble lekérése.
        
        Returns:
            Dict: Napi scramble adatok
        """
        try:
            response = requests.get(f"{self.api_url}/scramble/daily")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting daily scramble: {e}")
            return {"scramble": "Error getting daily scramble", "type": "daily", "length": 0}
    
    # ============= ALGORITHM METHODS =============
    
    def get_algorithms(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Algoritmusok listázása.
        
        Args:
            category: Opcionális kategória szűrő
        
        Returns:
            List[Dict]: Algoritmusok listája
        """
        try:
            params = {"category": category} if category else {}
            response = requests.get(f"{self.api_url}/algorithms", params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting algorithms: {e}")
            return []
    
    def get_algorithm(self, algorithm_id: int) -> Optional[Dict[str, Any]]:
        """
        Egy algoritmus lekérése ID alapján.
        
        Args:
            algorithm_id: Algoritmus azonosító
        
        Returns:
            Optional[Dict]: Algoritmus adatok vagy None
        """
        try:
            response = requests.get(f"{self.api_url}/algorithms/{algorithm_id}")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting algorithm {algorithm_id}: {e}")
            return None
    
    def create_algorithm(self, name: str, notation: str, category: str, difficulty: str) -> Optional[Dict[str, Any]]:
        """
        Új algoritmus létrehozása.
        
        Args:
            name: Algoritmus neve
            notation: Lépéssorozat
            category: Kategória
            difficulty: Nehézség
        
        Returns:
            Optional[Dict]: Létrehozott algoritmus vagy None
        """
        try:
            data = {
                "name": name,
                "notation": notation,
                "category": category,
                "difficulty": difficulty
            }
            response = requests.post(f"{self.api_url}/algorithms", json=data)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error creating algorithm: {e}")
            return None
    
    def delete_algorithm(self, algorithm_id: int) -> bool:
        """
        Algoritmus törlése.
        
        Args:
            algorithm_id: Törlendő algoritmus azonosító
        
        Returns:
            bool: True ha sikeres
        """
        try:
            response = requests.delete(f"{self.api_url}/algorithms/{algorithm_id}")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error deleting algorithm {algorithm_id}: {e}")
            return False
    
    def search_algorithms(self, query: str) -> List[Dict[str, Any]]:
        """
        Algoritmusok keresése.
        
        Args:
            query: Keresési kifejezés
        
        Returns:
            List[Dict]: Talált algoritmusok
        """
        try:
            response = requests.get(f"{self.api_url}/algorithms/search/{query}")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error searching algorithms: {e}")
            return []
    
    # ============= SOLVE TIME METHODS =============
    
    def save_time(self, time: float, scramble: str, dnf: int = 0) -> Optional[Dict[str, Any]]:
        """
        Kirakási idő mentése.
        
        Args:
            time: Idő másodpercben
            scramble: Használt scramble
            dnf: DNF jelző (0 vagy 1)
        
        Returns:
            Optional[Dict]: Mentett idő adatok
        """
        try:
            data = {
                "time": time,
                "scramble": scramble,
                "dnf": dnf
            }
            response = requests.post(f"{self.api_url}/times", json=data)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error saving time: {e}")
            return None
    
    def get_times(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Összes kirakási idő lekérése.
        
        Args:
            limit: Opcionális limit
        
        Returns:
            List[Dict]: Idők listája
        """
        try:
            params = {"limit": limit} if limit else {}
            response = requests.get(f"{self.api_url}/times", params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting times: {e}")
            return []
    
    def get_recent_times(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Legutóbbi idők lekérése.
        
        Args:
            limit: Visszaadott elemek száma
        
        Returns:
            List[Dict]: Legutóbbi idők
        """
        try:
            response = requests.get(f"{self.api_url}/times/recent/{limit}")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting recent times: {e}")
            return []
    
    # ============= STATISTICS METHODS =============
    
    def get_stats_summary(self) -> Dict[str, Any]:
        """
        Statisztika összesítő lekérése.
        
        Returns:
            Dict: Stats summary (best, ao5, ao12, ao100, total_solves)
        """
        try:
            response = requests.get(f"{self.api_url}/stats/summary")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting stats summary: {e}")
            return {
                "best": None,
                "ao5": None,
                "ao12": None,
                "ao100": None,
                "total_solves": 0
            }
    
    def get_chart_data(self) -> List[Dict[str, Any]]:
        """
        Grafikon adatok lekérése.
        
        Returns:
            List[Dict]: Chart data points
        """
        try:
            response = requests.get(f"{self.api_url}/stats/chart-data")
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting chart data: {e}")
            return []
    
    def get_distribution(self, bucket_size: float = 2.0) -> List[Dict[str, Any]]:
        """
        Idő eloszlás lekérése.
        
        Args:
            bucket_size: Bucket mérete
        
        Returns:
            List[Dict]: Distribution buckets
        """
        try:
            params = {"bucket_size": bucket_size}
            response = requests.get(f"{self.api_url}/stats/distribution", params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting distribution: {e}")
            return []
    
    def get_session_stats(self, hours: int = 24) -> Dict[str, Any]:
        """
        Session statisztikák lekérése.
        
        Args:
            hours: Visszamenőleges órák száma
        
        Returns:
            Dict: Session stats
        """
        try:
            params = {"hours": hours}
            response = requests.get(f"{self.api_url}/stats/session", params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting session stats: {e}")
            return {
                "period_hours": hours,
                "total_solves": 0,
                "valid_solves": 0,
                "best": None,
                "average": None
            }
    
    # ============= HEALTH CHECK =============
    
    def health_check(self) -> bool:
        """
        Backend health check.
        
        Returns:
            bool: True ha elérhető a backend
        """
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
