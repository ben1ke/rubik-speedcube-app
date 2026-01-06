"""
Konfiguráció kezelése environment változókból.
Pydantic Settings használatával típusbiztos konfigurációkezelés.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Alkalmazás konfigurációs beállítások.
    
    Attributes:
        database_url: SQLite adatbázis elérési útja
        api_host: API szerver host címe
        api_port: API szerver port száma
        backend_url: Teljes backend URL (frontendhez)
    """
    database_url: str = "sqlite:///./rubik_app.db"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    backend_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Singleton pattern a beállítások cache-eléséhez.
    
    Returns:
        Settings: Konfigurációs objektum
    """
    return Settings()
