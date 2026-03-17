"""
FunLearn - Main FastAPI Application
Powered by DigitalOcean Gradient AI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.api.routes import (
    auth,
    users,
    learning,
    quiz,
    admin,
    chat,
    characters,
    features,
    feynman,
    sessions,
    story_learning,
    video
)
from app.services.provider_factory import ProviderFactory
from app.utils.json_utils import NaNSafeJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    print("=" * 60)
    print("🚀 Starting FunLearn...")
    print("=" * 60)
    print(f"📦 AI Provider: {os.getenv('AI_PROVIDER', 'digitalocean')}")
    print(f"🖼️  Image Provider: {os.getenv('IMAGE_PROVIDER', 'none')}")
    print(f"🔊 TTS Provider: {os.getenv('VOICE_TTS_PROVIDER', 'none')}")
    print(f"🎤 STT Provider: {os.getenv('VOICE_STT_PROVIDER', 'none')}")
    print("-" * 60)

    # Check provider health
    try:
        print("Checking provider health...")
        status = await ProviderFactory.check_all_providers()
        for name, info in status.items():
            if info["status"] == "healthy":
                print(f"  ✅ {name}: {info['provider']} - {info['status']}")
            else:
                print(f"  ❌ {name}: {info['provider']} - {info['status']}")
                if "error" in info:
                    print(f"     Error: {info['error']}")
    except Exception as e:
        print(f"  ⚠️  Provider health check failed: {e}")

    print("=" * 60)
    print("✨ FunLearn is ready!")
    print(f"📚 API Documentation: http://{settings.BACKEND_HOST}:{settings.BACKEND_PORT}/docs")
    print("=" * 60)

    yield

    # Shutdown
    print("\n" + "=" * 60)
    print("👋 Shutting down FunLearn...")
    print("=" * 60)


app = FastAPI(
    title="FunLearn",
    description="Feynman AI for Every Student - Powered by DigitalOcean Gradient AI",
    version="2.0.0",
    lifespan=lifespan,
    default_response_class=NaNSafeJSONResponse  # Handle NaN values globally
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://[::1]:5173",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for media
if settings.MEDIA_DIR.exists():
    app.mount("/media", StaticFiles(directory=str(settings.MEDIA_DIR)), name="media")

# Mount static files for MCT images
from pathlib import Path
mct_data_dir = Path(__file__).parent.parent / "data"
if mct_data_dir.exists():
    app.mount("/data", StaticFiles(directory=str(mct_data_dir)), name="data")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(features.router, prefix="/api/features", tags=["MCT Diagnostics"])
app.include_router(feynman.router, prefix="/api")  # Feynman Engine
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(video.router, prefix="/api/video", tags=["Video"])
app.include_router(characters.router, prefix="/api/characters", tags=["Characters"])
app.include_router(story_learning.router)  # Story Learning


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to FunLearn!",
        "version": "2.0.0",
        "description": "Feynman AI for Every Student - Powered by DigitalOcean Gradient AI",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint

    Returns system status and provider health
    """
    try:
        providers = await ProviderFactory.check_all_providers()
        all_healthy = all(p["status"] == "healthy" for p in providers.values())

        return {
            "status": "healthy" if all_healthy else "degraded",
            "providers": providers,
            "version": "2.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "version": "2.0.0"
        }
