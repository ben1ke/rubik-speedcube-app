"""
FastAPI alkalmazás belépési pontja.
REST API inicializálás és middleware beállítások.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.database import init_db
from backend.config import get_settings

# Logging beállítása
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Beállítások
settings = get_settings()

# FastAPI app létrehozása
app = FastAPI(
    title="Rubik Speedcube API",
    description="REST API Rubik kocka speedcubing alkalmazáshoz",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (Streamlit frontend számára)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Éles környezetben specifikáljuk!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Alkalmazás indításkor végrehajtandó műveletek.
    Adatbázis inicializálása és táblák létrehozása.
    """
    logger.info("Starting Rubik Speedcube API...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """
    Alkalmazás leállításkor végrehajtandó műveletek.
    """
    logger.info("Shutting down Rubik Speedcube API...")


@app.get("/")
async def root():
    """
    Health check endpoint.
    
    Returns:
        dict: API státusz és verzió információk
    """
    return {
        "message": "Rubik Speedcube API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Részletes health check endpoint.
    
    Returns:
        dict: Rendszer állapot információk
    """
    return {
        "status": "healthy",
        "database": "connected",
        "api_version": "1.0.0"
    }


# Router-ek regisztrálása
from backend.api.routes import router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
