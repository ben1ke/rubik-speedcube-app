"""
Pydantic sémák API request/response validációhoz.
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


# ============= ALGORITHM SCHEMÁK =============

class AlgorithmBase(BaseModel):
    """Közös algoritmus mezők."""
    name: str = Field(..., min_length=1, max_length=100, description="Algoritmus neve")
    notation: str = Field(..., min_length=1, max_length=500, description="Lépéssorozat")
    category: str = Field(..., min_length=1, max_length=50, description="Kategória (PLL, OLL, F2L)")
    difficulty: str = Field(default="Kezdő", description="Nehézség (Kezdő, Haladó, Expert)")
    
    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        """Nehézségi szint validáció."""
        allowed = ["Kezdő", "Haladó", "Expert"]
        if v not in allowed:
            raise ValueError(f"Difficulty must be one of: {', '.join(allowed)}")
        return v
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        """Kategória validáció."""
        allowed = ["PLL", "OLL", "F2L", "CMLL", "COLL", "Basic", "Advanced"]
        if v not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(allowed)}")
        return v


class AlgorithmCreate(AlgorithmBase):
    """Algoritmus létrehozásához szükséges séma."""
    pass


class AlgorithmResponse(AlgorithmBase):
    """Algoritmus válasz séma (id és created_at-tal)."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= SOLVE TIME SCHEMÁK =============

class SolveTimeBase(BaseModel):
    """Közös kirakási idő mezők."""
    time: float = Field(..., gt=0, description="Kirakási idő másodpercben")
    scramble: str = Field(..., min_length=1, max_length=500, description="Használt keverés")
    dnf: int = Field(default=0, ge=0, le=1, description="DNF jelző (0=sikeres, 1=DNF)")
    
    @field_validator('dnf')
    @classmethod
    def validate_dnf(cls, v: int) -> int:
        """DNF validáció."""
        if v not in [0, 1]:
            raise ValueError("DNF must be 0 or 1")
        return v


class SolveTimeCreate(SolveTimeBase):
    """Kirakási idő létrehozásához szükséges séma."""
    pass


class SolveTimeResponse(SolveTimeBase):
    """Kirakási idő válasz séma."""
    id: int
    date: datetime
    
    class Config:
        from_attributes = True


# ============= SCRAMBLE SCHEMÁK =============

class ScrambleBase(BaseModel):
    """Közös keverés mezők."""
    scramble: str = Field(..., min_length=1, max_length=500, description="Keverés notációban")
    used: int = Field(default=0, ge=0, le=1, description="Használva volt-e (0=nem, 1=igen)")


class ScrambleCreate(ScrambleBase):
    """Keverés létrehozásához szükséges séma."""
    pass


class ScrambleResponse(ScrambleBase):
    """Keverés válasz séma."""
    id: int
    date: datetime
    
    class Config:
        from_attributes = True


# ============= STATISZTIKA SCHEMÁK =============

class StatsResponse(BaseModel):
    """Statisztika összesítő válasz."""
    best: Optional[float] = Field(None, description="Legjobb idő")
    ao5: Optional[float] = Field(None, description="Average of 5")
    ao12: Optional[float] = Field(None, description="Average of 12")
    ao100: Optional[float] = Field(None, description="Average of 100")
    total_solves: int = Field(..., description="Összes kirakás")
    
    class Config:
        from_attributes = True


class ChartDataPoint(BaseModel):
    """Egy adatpont a grafikonhoz."""
    date: datetime
    time: float
    solve_number: int
    
    class Config:
        from_attributes = True


class DistributionBucket(BaseModel):
    """Idő eloszlás bucket."""
    range: str = Field(..., description="Időtartomány (pl. '10-12s')")
    count: int = Field(..., description="Kirakások száma ebben a tartományban")
