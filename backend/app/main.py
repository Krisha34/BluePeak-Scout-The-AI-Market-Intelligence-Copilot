"""
FastAPI main application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logger import app_logger
from app.api.endpoints import competitors, trends, chat, reports, integrations, analytics
from app.api.websocket import websocket_router


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-agent AI platform for competitive intelligence and market research",
    version="0.1.0",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    competitors.router,
    prefix=f"{settings.API_PREFIX}/competitors",
    tags=["competitors"]
)
app.include_router(
    trends.router,
    prefix=f"{settings.API_PREFIX}/trends",
    tags=["trends"]
)
app.include_router(
    chat.router,
    prefix=f"{settings.API_PREFIX}/chat",
    tags=["chat"]
)
app.include_router(
    reports.router,
    prefix=f"{settings.API_PREFIX}/reports",
    tags=["reports"]
)
app.include_router(
    integrations.router,
    prefix=f"{settings.API_PREFIX}/integrations",
    tags=["integrations"]
)
app.include_router(
    analytics.router,
    prefix=f"{settings.API_PREFIX}/analytics",
    tags=["analytics"]
)
app.include_router(
    websocket_router,
    prefix="/ws",
    tags=["websocket"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "status": "operational",
        "docs": f"{settings.API_PREFIX}/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    app_logger.info(f"Starting {settings.APP_NAME}")
    app_logger.info(f"Environment: {settings.ENVIRONMENT}")
    app_logger.info(f"API Prefix: {settings.API_PREFIX}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown tasks"""
    app_logger.info(f"Shutting down {settings.APP_NAME}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    app_logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
