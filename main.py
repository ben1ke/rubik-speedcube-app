"""
FastAPI Backend - REST API
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import logging
import os
from dotenv import load_dotenv

from models import (
    init_db, get_db, 
    SolveTimeCreate, SolveTimeResponse, 
    ScrambleResponse, StatsResponse
)
from services import TimerService, ScrambleService, generate_scramble

# Konfiguráció
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Rubik Speedcube API",
    description="REST API Rubik kocka időméréshez",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Alkalmazás indítás - adatbázis inicializálás."""
    logger.info("Starting Speedcube API...")
    init_db()
    logger.info("Database initialized")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Rubik Speedcube API",
        "version": "1.0.0",
        "endpoints": ["/scramble", "/times", "/stats"]
    }


@app.get("/scramble", response_model=dict)
async def get_scramble(db: Session = Depends(get_db)):
    """Új scramble generálása - PROCEDURÁLIS."""
    scramble = generate_scramble()
    return {"scramble": scramble}


@app.get("/scramble/daily", response_model=dict)
async def get_daily_scramble(db: Session = Depends(get_db)):
    """Napi scramble lekérése - OOP."""
    service = ScrambleService(db)
    scramble = service.get_daily_scramble()
    return {"scramble": scramble}


@app.post("/times", response_model=SolveTimeResponse)
async def save_time(
    solve_data: SolveTimeCreate,
    db: Session = Depends(get_db)
):
    """Solve time mentése - OOP."""
    service = TimerService(db)
    solve = service.save_time(solve_data.time, solve_data.scramble)
    return solve


@app.get("/times", response_model=List[SolveTimeResponse])
async def get_times(db: Session = Depends(get_db)):
    """Összes solve time lekérése - OOP."""
    service = TimerService(db)
    times = service.get_all_times()
    return times


@app.get("/stats", response_model=StatsResponse)
async def get_statistics(db: Session = Depends(get_db)):
    """Statisztikák lekérése - OOP + FUNKCIONÁLIS."""
    service = TimerService(db)
    stats = service.get_statistics()
    return stats


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
