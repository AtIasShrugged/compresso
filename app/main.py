"""Main FastAPI application."""
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

from .config import settings
from .web.routes import pages_router
from .infra.cache import redis_cache


# Configure logging
logger.remove()
if settings.is_prod:
    # JSON logging for production
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        serialize=True
    )
else:
    # Pretty logging for development
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG"
    )

logger.info(f"Starting Compresso in {settings.app_env} mode")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Application startup")
    await redis_cache.connect()
    
    yield
    
    # Shutdown
    logger.info("Application shutdown")
    await redis_cache.disconnect()


# Create FastAPI app
app = FastAPI(
    title="Compresso",
    description="Fast LLM Summarizer for Text, Articles, and YouTube videos",
    version="1.0.0",
    docs_url="/api/docs" if settings.is_dev else None,
    redoc_url="/api/redoc" if settings.is_dev else None,
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

# Include routers
app.include_router(pages_router)


@app.get("/api/info")
async def info():
    """API information endpoint."""
    return {
        "name": "Compresso",
        "version": "1.0.0",
        "environment": settings.app_env
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_dev
    )
