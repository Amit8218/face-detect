from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb+srv://aj9858575_db_user:hC5lPalFHDjmCEbH@cluster0.zpfq7ew.mongodb.net/?appName=Cluster0"
    DATABASE_NAME: str = "face_recognition_db"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:8001", "http://127.0.0.1:8001" ,"http://localhost:5500","http://127.0.0.1:5500"]
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Face Recognition API"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
