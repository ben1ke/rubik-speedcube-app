"""
API Router - FastAPI végpontok definíciója.
Összes REST API endpoint a Rubik Speedcube alkalmazáshoz.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from backend.database import get_db
from backend.services.algorithm_service import AlgorithmService
from backend.services.timer_service import TimerService, generate_scramble
from backend.services.stats_service import StatsService
from backend.schemas.schemas import (
    AlgorithmCreate,
    AlgorithmResponse,
    SolveTimeCreate,
    SolveTimeResponse,
    ScrambleResponse,
    StatsResponse,
    ChartDataPoint,
    DistributionBucket
)

logger = logging.getLogger(__name__)

# Router létrehozása
router = APIRouter(prefix="/api", tags=["api"])


# ============= SCRAMBLE ENDPOINTS =============

@router.get("/scramble", response_model=dict)
async def get_random_scramble():
    """
    Random scramble generálása.
    Procedurális függvény használata a scramble generáláshoz.
    
    Returns:
        dict: Generált scramble
    """
    try:
        # Procedurális függvény hívása
        scramble = generate_scramble()
        logger.info("Generated random scramble via API")
        return {
            "scramble": scramble,
            "length": len(scramble.split())
        }
    except Exception as e:
        logger.error(f"Error generating scramble: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate scramble")


@router.get("/scramble/daily", response_model=dict)
async def get_daily_scramble(db: Session = Depends(get_db)):
    """
    Napi scramble lekérése.
    Ha már volt ma, azt adja vissza, különben újat generál.
    
    Args:
        db: Database session (dependency injection)
    
    Returns:
        dict: Napi scramble
    """
    try:
        timer_service = TimerService(db)
        daily_scramble = timer_service.get_daily_scramble()
        logger.info("Retrieved daily scramble via API")
        return {
            "scramble": daily_scramble,
            "type": "daily",
            "length": len(daily_scramble.split())
        }
    except Exception as e:
        logger.error(f"Error getting daily scramble: {e}")
        raise HTTPException(status_code=500, detail="Failed to get daily scramble")


# ============= ALGORITHM ENDPOINTS =============

@router.get("/algorithms", response_model=List[AlgorithmResponse])
async def get_algorithms(
    category: Optional[str] = Query(None, description="Szűrés kategória szerint (PLL, OLL, F2L, stb.)"),
    db: Session = Depends(get_db)
):
    """
    Algoritmusok listázása, opcionális kategória szűréssel.
    
    Args:
        category: Opcionális kategória szűrő
        db: Database session
    
    Returns:
        List[AlgorithmResponse]: Algoritmusok listája
    """
    try:
        algorithm_service = AlgorithmService(db)
        algorithms = algorithm_service.get_all(category=category)
        logger.info(f"Retrieved {len(algorithms)} algorithms via API")
        return algorithms
    except Exception as e:
        logger.error(f"Error getting algorithms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve algorithms")


@router.get("/algorithms/{algorithm_id}", response_model=AlgorithmResponse)
async def get_algorithm(algorithm_id: int, db: Session = Depends(get_db)):
    """
    Egy algoritmus lekérése ID alapján.
    
    Args:
        algorithm_id: Algoritmus azonosító
        db: Database session
    
    Returns:
        AlgorithmResponse: Algoritmus adatok
    
    Raises:
        HTTPException: 404 ha nem található
    """
    try:
        algorithm_service = AlgorithmService(db)
        algorithm = algorithm_service.get_by_id(algorithm_id)
        
        if not algorithm:
            raise HTTPException(status_code=404, detail=f"Algorithm not found with id: {algorithm_id}")
        
        logger.info(f"Retrieved algorithm {algorithm_id} via API")
        return algorithm
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting algorithm {algorithm_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve algorithm")


@router.post("/algorithms", response_model=AlgorithmResponse, status_code=201)
async def create_algorithm(
    algorithm: AlgorithmCreate,
    db: Session = Depends(get_db)
):
    """
    Új algoritmus létrehozása.
    
    Args:
        algorithm: Algoritmus adatok (Pydantic schema validációval)
        db: Database session
    
    Returns:
        AlgorithmResponse: Létrehozott algoritmus
    
    Raises:
        HTTPException: 400 ha már létezik ilyen nevű algoritmus
    """
    try:
        algorithm_service = AlgorithmService(db)
        new_algorithm = algorithm_service.create(algorithm)
        logger.info(f"Created algorithm '{new_algorithm.name}' via API")
        return new_algorithm
    except ValueError as ve:
        logger.warning(f"Algorithm creation failed: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error creating algorithm: {e}")
        raise HTTPException(status_code=500, detail="Failed to create algorithm")


@router.delete("/algorithms/{algorithm_id}", status_code=204)
async def delete_algorithm(algorithm_id: int, db: Session = Depends(get_db)):
    """
    Algoritmus törlése ID alapján.
    
    Args:
        algorithm_id: Törlendő algoritmus azonosító
        db: Database session
    
    Raises:
        HTTPException: 404 ha nem található
    """
    try:
        algorithm_service = AlgorithmService(db)
        success = algorithm_service.delete(algorithm_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Algorithm not found with id: {algorithm_id}")
        
        logger.info(f"Deleted algorithm {algorithm_id} via API")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting algorithm {algorithm_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete algorithm")


@router.get("/algorithms/search/{query}", response_model=List[AlgorithmResponse])
async def search_algorithms(query: str, db: Session = Depends(get_db)):
    """
    Algoritmusok keresése név alapján.
    Funkcionális paradigma használata a service-ben.
    
    Args:
        query: Keresési kifejezés
        db: Database session
    
    Returns:
        List[AlgorithmResponse]: Talált algoritmusok
    """
    try:
        algorithm_service = AlgorithmService(db)
        results = algorithm_service.search(query)
        logger.info(f"Search for '{query}' returned {len(results)} results via API")
        return results
    except Exception as e:
        logger.error(f"Error searching algorithms: {e}")
        raise HTTPException(status_code=500, detail="Failed to search algorithms")


# ============= TIMER / SOLVE TIME ENDPOINTS =============

@router.post("/times", response_model=SolveTimeResponse, status_code=201)
async def save_solve_time(
    solve_time: SolveTimeCreate,
    db: Session = Depends(get_db)
):
    """
    Kirakási idő mentése.
    
    Args:
        solve_time: Idő adatok (Pydantic schema validációval)
        db: Database session
    
    Returns:
        SolveTimeResponse: Mentett idő
    
    Raises:
        HTTPException: 400 ha érvénytelen idő érték
    """
    try:
        timer_service = TimerService(db)
        new_time = timer_service.save_time(solve_time)
        logger.info(f"Saved solve time via API: {new_time.time}s")
        return new_time
    except ValueError as ve:
        logger.warning(f"Invalid solve time: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error saving solve time: {e}")
        raise HTTPException(status_code=500, detail="Failed to save solve time")


@router.get("/times", response_model=List[SolveTimeResponse])
async def get_all_times(
    limit: Optional[int] = Query(None, description="Maximális visszaadott elemek száma"),
    db: Session = Depends(get_db)
):
    """
    Összes kirakási idő lekérése.
    
    Args:
        limit: Opcionális limit
        db: Database session
    
    Returns:
        List[SolveTimeResponse]: Idők listája (legújabb először)
    """
    try:
        timer_service = TimerService(db)
        times = timer_service.get_all_times(limit=limit)
        logger.info(f"Retrieved {len(times)} solve times via API")
        return times
    except Exception as e:
        logger.error(f"Error getting solve times: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve solve times")


@router.get("/times/{time_id}", response_model=SolveTimeResponse)
async def get_solve_time(time_id: int, db: Session = Depends(get_db)):
    """
    Egy kirakási idő lekérése ID alapján.
    
    Args:
        time_id: Idő azonosító
        db: Database session
    
    Returns:
        SolveTimeResponse: Idő adatok
    
    Raises:
        HTTPException: 404 ha nem található
    """
    try:
        timer_service = TimerService(db)
        solve_time = timer_service.get_by_id(time_id)
        
        if not solve_time:
            raise HTTPException(status_code=404, detail=f"Solve time not found with id: {time_id}")
        
        logger.info(f"Retrieved solve time {time_id} via API")
        return solve_time
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting solve time {time_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve solve time")


@router.get("/times/recent/{limit}", response_model=List[SolveTimeResponse])
async def get_recent_times(limit: int = 10, db: Session = Depends(get_db)):
    """
    Legutóbbi N kirakási idő lekérése.
    
    Args:
        limit: Visszaadott elemek száma
        db: Database session
    
    Returns:
        List[SolveTimeResponse]: Legutóbbi idők
    """
    try:
        timer_service = TimerService(db)
        times = timer_service.get_recent(limit=limit)
        logger.info(f"Retrieved {len(times)} recent times via API")
        return times
    except Exception as e:
        logger.error(f"Error getting recent times: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recent times")


# ============= STATISTICS ENDPOINTS =============

@router.get("/stats/summary", response_model=StatsResponse)
async def get_stats_summary(db: Session = Depends(get_db)):
    """
    Teljes statisztika összesítő.
    Funkcionális paradigma használata a számításokban (map, filter, reduce).
    
    Args:
        db: Database session
    
    Returns:
        StatsResponse: Összesített statisztikák (best, ao5, ao12, ao100, total)
    """
    try:
        stats_service = StatsService(db)
        summary = stats_service.get_summary()
        logger.info("Retrieved stats summary via API")
        return summary
    except Exception as e:
        logger.error(f"Error getting stats summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")


@router.get("/stats/chart-data", response_model=List[ChartDataPoint])
async def get_chart_data(db: Session = Depends(get_db)):
    """
    Grafikon adatok lekérése időfejlődéshez.
    Funkcionális paradigma a service-ben.
    
    Args:
        db: Database session
    
    Returns:
        List[ChartDataPoint]: Adatpontok grafikonhoz
    """
    try:
        stats_service = StatsService(db)
        chart_data = stats_service.get_chart_data()
        logger.info(f"Retrieved {len(chart_data)} chart data points via API")
        return chart_data
    except Exception as e:
        logger.error(f"Error getting chart data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chart data")


@router.get("/stats/distribution", response_model=List[DistributionBucket])
async def get_distribution(
    bucket_size: float = Query(2.0, description="Bucket mérete másodpercekben"),
    db: Session = Depends(get_db)
):
    """
    Idő eloszlás bucket-ekre osztva.
    Funkcionális paradigma használata a service-ben.
    
    Args:
        bucket_size: Bucket szélessége (másodpercben)
        db: Database session
    
    Returns:
        List[DistributionBucket]: Eloszlás bucket-ek
    """
    try:
        stats_service = StatsService(db)
        distribution = stats_service.get_distribution(bucket_size=bucket_size)
        logger.info(f"Retrieved distribution with {len(distribution)} buckets via API")
        return distribution
    except Exception as e:
        logger.error(f"Error getting distribution: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve distribution")


@router.get("/stats/session", response_model=dict)
async def get_session_stats(
    hours: int = Query(24, description="Visszamenőleges órák száma"),
    db: Session = Depends(get_db)
):
    """
    Session statisztikák (pl. utolsó 24 óra).
    
    Args:
        hours: Időszak órákban
        db: Database session
    
    Returns:
        dict: Session statisztikák
    """
    try:
        stats_service = StatsService(db)
        session_stats = stats_service.get_session_stats(hours=hours)
        logger.info(f"Retrieved session stats for last {hours} hours via API")
        return session_stats
    except Exception as e:
        logger.error(f"Error getting session stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve session statistics")


# ============= UTILITY ENDPOINTS =============

@router.get("/algorithms/grouped/by-category", response_model=dict)
async def get_algorithms_grouped(db: Session = Depends(get_db)):
    """
    Algoritmusok kategóriák szerint csoportosítva.
    Funkcionális paradigma a service-ben.
    
    Args:
        db: Database session
    
    Returns:
        dict: Kategóriák szerint csoportosított algoritmusok
    """
    try:
        algorithm_service = AlgorithmService(db)
        grouped = algorithm_service.get_by_category_grouped()
        
        # Alakítsuk át serializable formátumra
        result = {}
        for category, algorithms in grouped.items():
            result[category] = [
                {
                    "id": alg.id,
                    "name": alg.name,
                    "notation": alg.notation,
                    "difficulty": alg.difficulty
                }
                for alg in algorithms
            ]
        
        logger.info(f"Retrieved algorithms grouped by {len(result)} categories via API")
        return result
    except Exception as e:
        logger.error(f"Error getting grouped algorithms: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve grouped algorithms")
