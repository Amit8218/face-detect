from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from routes import face_routes
import os
from pathlib import Path

# Get the directory where this file is located
BASE_DIR = Path(__file__).resolve().parent

# Database client
mongodb_client = None
database = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global mongodb_client, database
    mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = mongodb_client[settings.DATABASE_NAME]
    app.state.db = database
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")
    
    yield
    
    # Shutdown
    mongodb_client.close()
    print("Disconnected from MongoDB")

app = FastAPI(
    title="Face Recognition API",
    description="Backend API for face registration and recognition system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.CORS_ORIGINS,
    allow_origins=
    [
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(face_routes.router, prefix="/api/v1", tags=["Face Recognition"])

# Mount static files (HTML, CSS, JS, models)
app.mount("/models", StaticFiles(directory=str(BASE_DIR / "models")), name="models")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# Serve frontend HTML files
@app.get("/")
async def serve_root():
    return FileResponse(BASE_DIR / "registerFace.html", media_type="text/html")

@app.get("/register")
async def serve_register():
    return FileResponse(BASE_DIR / "registerFace.html", media_type="text/html")

@app.get("/view")
async def serve_view():
    return FileResponse(BASE_DIR / "viewFaces.html", media_type="text/html")

# Mount root directory for static files (JS, CSS, etc.)
# This should be after specific routes so they take priority
app.mount("", StaticFiles(directory=str(BASE_DIR), html=False), name="static")
