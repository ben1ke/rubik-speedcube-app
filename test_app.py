"""
Pytest tesztek - 3 teszt, 1 parametrize
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from models import Base, SolveTime
from services import (
    generate_scramble, 
    calculate_average,
    TimerService
)


# Test database fixture
@pytest.fixture
def test_db():
    """Test adatbázis fixture."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


# ============================================
# TESZT 1: Procedurális scramble generálás
# ============================================
def test_generate_scramble():
    """
    Teszt: Procedurális scramble generálás működik.
    """
    scramble = generate_scramble(20)
    
    assert scramble is not None
    assert isinstance(scramble, str)
    assert len(scramble.split()) == 20
    assert all(move[0] in "RLUDFB" for move in scramble.split())


# ============================================
# TESZT 2: Funkcionális átlagszámítás - PARAMETRIZE
# ============================================
@pytest.mark.parametrize("times,expected", [
    ([10.0, 12.0, 11.0], 11.0),
    ([5.5, 6.5, 7.5], 6.5),
    ([15.0, 15.0, 15.0], 15.0),
    ([8.0], 8.0),
])
def test_calculate_average_parametrized(times, expected):
    """
    Teszt: Funkcionális átlagszámítás különböző input esetekre.
    @pytest.mark.parametrize használatával.
    """
    result = calculate_average(times)
    assert result == pytest.approx(expected, rel=0.01)


# ============================================
# TESZT 3: OOP TimerService mentés
# ============================================
def test_timer_service_save(test_db):
    """
    Teszt: OOP TimerService idő mentése működik.
    """
    service = TimerService(test_db)
    
    # Idő mentése
    solve = service.save_time(12.34, "R U R' U'")
    
    assert solve.id is not None
    assert solve.time == 12.34
    assert solve.scramble == "R U R' U'"
    
    # Lekérdezés
    all_times = service.get_all_times()
    assert len(all_times) == 1
    assert all_times[0].time == 12.34
