"""
Stats Service - Statisztika számítások.
Funkcionális paradigma: map, filter, reduce, lambda használata.
OOP paradigma: Osztály alapú service layer.
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from functools import reduce
from datetime import datetime, timedelta
import logging

from backend.models.models import SolveTime
from backend.schemas.schemas import StatsResponse, ChartDataPoint, DistributionBucket

logger = logging.getLogger(__name__)


class StatsService:
    """
    Statisztika számítások service osztálya.
    OOP PARADIGMA: Osztály alapú architektúra.
    FUNKCIONÁLIS PARADIGMA: map, filter, reduce, lambda használata.
    """
    
    def __init__(self, db: Session):
        """
        Service inicializálása database session-nel.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def _get_valid_times(self) -> List[SolveTime]:
        """
        Érvényes (nem DNF) idők lekérése az adatbázisból.
        FUNKCIONÁLIS PARADIGMA: filter használata.
        
        Returns:
            List[SolveTime]: Érvényes kirakási idők
        """
        try:
            all_times = self.db.query(SolveTime).order_by(SolveTime.date.desc()).all()
            
            # FUNKCIONÁLIS PARADIGMA: Filter + lambda
            # DNF-ek kiszűrése (dnf == 0 csak érvényes)
            valid_times = list(filter(lambda t: t.dnf == 0, all_times))
            
            logger.info(f"Filtered {len(valid_times)} valid times from {len(all_times)} total")
            return valid_times
        except Exception as e:
            logger.error(f"Error getting valid times: {e}")
            raise
    
    def _extract_time_values(self, times: List[SolveTime]) -> List[float]:
        """
        Idő értékek kinyerése SolveTime objektumokból.
        FUNKCIONÁLIS PARADIGMA: map használata.
        
        Args:
            times: SolveTime objektumok listája
        
        Returns:
            List[float]: Idő értékek listája
        """
        # FUNKCIONÁLIS PARADIGMA: Map + lambda
        time_values = list(map(lambda t: t.time, times))
        return time_values
    
    def calculate_best(self, times: Optional[List[SolveTime]] = None) -> Optional[float]:
        """
        Legjobb idő kiszámítása.
        FUNKCIONÁLIS PARADIGMA: min() használata.
        
        Args:
            times: Opcionális idők listája (None esetén lekéri az adatbázisból)
        
        Returns:
            Optional[float]: Legjobb idő vagy None ha nincs adat
        """
        try:
            if times is None:
                times = self._get_valid_times()
            
            if not times:
                return None
            
            # FUNKCIONÁLIS PARADIGMA: Map + min
            time_values = self._extract_time_values(times)
            best = min(time_values) if time_values else None
            
            if best:
                logger.info(f"Best time: {best:.2f}s")
            
            return best
        except Exception as e:
            logger.error(f"Error calculating best time: {e}")
            return None
    
    def calculate_average(self, times: List[float]) -> float:
        """
        Egyszerű átlag számítás.
        FUNKCIONÁLIS PARADIGMA: reduce használata.
        
        Args:
            times: Idő értékek listája
        
        Returns:
            float: Átlag idő
        """
        if not times:
            return 0.0
        
        # FUNKCIONÁLIS PARADIGMA: Reduce + lambda
        total = reduce(lambda x, y: x + y, times, 0.0)
        average = total / len(times)
        
        return round(average, 2)
    
    def calculate_ao5(self, times: Optional[List[SolveTime]] = None) -> Optional[float]:
        """
        Average of 5 számítás (legjobb és legrosszabb kihagyásával).
        FUNKCIONÁLIS PARADIGMA: Kombinált használat.
        
        Args:
            times: Opcionális idők listája
        
        Returns:
            Optional[float]: AO5 érték vagy None
        """
        try:
            if times is None:
                times = self._get_valid_times()
            
            if len(times) < 5:
                logger.info("Not enough times for AO5 calculation (need 5)")
                return None
            
            # Utolsó 5 idő
            last_5 = times[:5]
            time_values = self._extract_time_values(last_5)
            
            # FUNKCIONÁLIS PARADIGMA: sorted + list slicing
            sorted_times = sorted(time_values)
            
            # Legjobb és legrosszabb kihagyása
            middle_3 = sorted_times[1:-1]
            
            # Átlag számítás reduce-szal
            ao5 = self.calculate_average(middle_3)
            
            logger.info(f"AO5: {ao5:.2f}s")
            return ao5
        except Exception as e:
            logger.error(f"Error calculating AO5: {e}")
            return None
    
    def calculate_ao12(self, times: Optional[List[SolveTime]] = None) -> Optional[float]:
        """
        Average of 12 számítás (legjobb és legrosszabb kihagyásával).
        FUNKCIONÁLIS PARADIGMA: Hasonló az AO5-höz.
        
        Args:
            times: Opcionális idők listája
        
        Returns:
            Optional[float]: AO12 érték vagy None
        """
        try:
            if times is None:
                times = self._get_valid_times()
            
            if len(times) < 12:
                logger.info("Not enough times for AO12 calculation (need 12)")
                return None
            
            # Utolsó 12 idő
            last_12 = times[:12]
            time_values = self._extract_time_values(last_12)
            
            # FUNKCIONÁLIS PARADIGMA: sorted
            sorted_times = sorted(time_values)
            
            # Legjobb és legrosszabb kihagyása
            middle_10 = sorted_times[1:-1]
            
            ao12 = self.calculate_average(middle_10)
            
            logger.info(f"AO12: {ao12:.2f}s")
            return ao12
        except Exception as e:
            logger.error(f"Error calculating AO12: {e}")
            return None
    
    def calculate_ao100(self, times: Optional[List[SolveTime]] = None) -> Optional[float]:
        """
        Average of 100 számítás (legjobb 5 és legrosszabb 5 kihagyásával).
        FUNKCIONÁLIS PARADIGMA: Komplex szűrés és számítás.
        
        Args:
            times: Opcionális idők listája
        
        Returns:
            Optional[float]: AO100 érték vagy None
        """
        try:
            if times is None:
                times = self._get_valid_times()
            
            if len(times) < 100:
                logger.info("Not enough times for AO100 calculation (need 100)")
                return None
            
            # Utolsó 100 idő
            last_100 = times[:100]
            time_values = self._extract_time_values(last_100)
            
            # FUNKCIONÁLIS PARADIGMA: sorted
            sorted_times = sorted(time_values)
            
            # Legjobb 5 és legrosszabb 5 kihagyása
            middle_90 = sorted_times[5:-5]
            
            ao100 = self.calculate_average(middle_90)
            
            logger.info(f"AO100: {ao100:.2f}s")
            return ao100
        except Exception as e:
            logger.error(f"Error calculating AO100: {e}")
            return None
    
    def get_summary(self) -> StatsResponse:
        """
        Teljes statisztika összesítő.
        
        Returns:
            StatsResponse: Összesített statisztikák
        """
        try:
            valid_times = self._get_valid_times()
            all_times = self.db.query(SolveTime).all()
            
            summary = StatsResponse(
                best=self.calculate_best(valid_times),
                ao5=self.calculate_ao5(valid_times),
                ao12=self.calculate_ao12(valid_times),
                ao100=self.calculate_ao100(valid_times),
                total_solves=len(all_times)
            )
            
            logger.info(f"Generated stats summary: {summary.total_solves} solves")
            return summary
        except Exception as e:
            logger.error(f"Error generating stats summary: {e}")
            raise
    
    def get_chart_data(self) -> List[ChartDataPoint]:
        """
        Grafikon adatok előállítása időfejlődéshez.
        FUNKCIONÁLIS PARADIGMA: Map használata.
        
        Returns:
            List[ChartDataPoint]: Adatpontok listája grafikonhoz
        """
        try:
            valid_times = self._get_valid_times()
            
            # FUNKCIONÁLIS PARADIGMA: Map + lambda + enumerate
            # Minden időhöz hozzárendeljük a solve számot és formázzuk
            chart_data = list(map(
                lambda item: ChartDataPoint(
                    date=item[1].date,
                    time=item[1].time,
                    solve_number=len(valid_times) - item[0]
                ),
                enumerate(reversed(valid_times))
            ))
            
            logger.info(f"Generated {len(chart_data)} chart data points")
            return chart_data
        except Exception as e:
            logger.error(f"Error generating chart data: {e}")
            raise
    
    def get_distribution(self, bucket_size: float = 2.0) -> List[DistributionBucket]:
        """
        Idő eloszlás számítása bucket-ekre osztva.
        FUNKCIONÁLIS PARADIGMA: Filter + reduce-szerű csoportosítás.
        
        Args:
            bucket_size: Bucket mérete másodpercekben (pl. 2.0 = 2s széles bucket-ek)
        
        Returns:
            List[DistributionBucket]: Eloszlás bucket-ek
        """
        try:
            valid_times = self._get_valid_times()
            
            if not valid_times:
                return []
            
            time_values = self._extract_time_values(valid_times)
            
            # Min és max idők
            min_time = min(time_values)
            max_time = max(time_values)
            
            # Bucket-ek létrehozása
            buckets = {}
            current = int(min_time)
            
            while current <= max_time + bucket_size:
                bucket_key = f"{current}-{current + bucket_size}s"
                
                # FUNKCIONÁLIS PARADIGMA: Filter + lambda
                # Számoljuk meg hány idő esik ebbe a bucket-be
                count = len(list(filter(
                    lambda t: current <= t < current + bucket_size,
                    time_values
                )))
                
                if count > 0:
                    buckets[bucket_key] = count
                
                current += int(bucket_size)
            
            # Alakítsuk át DistributionBucket objektumokká
            distribution = [
                DistributionBucket(range=key, count=count)
                for key, count in buckets.items()
            ]
            
            logger.info(f"Generated distribution with {len(distribution)} buckets")
            return distribution
        except Exception as e:
            logger.error(f"Error calculating distribution: {e}")
            raise
    
    def get_session_stats(self, hours: int = 24) -> Dict:
        """
        Adott időszak statisztikái (pl. utolsó 24 óra).
        FUNKCIONÁLIS PARADIGMA: Filter időszűréssel.
        
        Args:
            hours: Visszamenőleges órák száma
        
        Returns:
            Dict: Session statisztikák
        """
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Összes idő az adott időszakban
            all_session_times = self.db.query(SolveTime).filter(
                SolveTime.date >= cutoff_time
            ).order_by(SolveTime.date.desc()).all()
            
            # FUNKCIONÁLIS PARADIGMA: Filter DNF-ekre
            valid_session_times = list(filter(lambda t: t.dnf == 0, all_session_times))
            
            if not valid_session_times:
                return {
                    "period_hours": hours,
                    "total_solves": len(all_session_times),
                    "valid_solves": 0,
                    "best": None,
                    "average": None
                }
            
            time_values = self._extract_time_values(valid_session_times)
            
            return {
                "period_hours": hours,
                "total_solves": len(all_session_times),
                "valid_solves": len(valid_session_times),
                "best": min(time_values),
                "average": self.calculate_average(time_values)
            }
        except Exception as e:
            logger.error(f"Error calculating session stats: {e}")
            raise
