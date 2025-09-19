from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import uvicorn

from app.core.config import settings
from app.core.database import connect_db, disconnect_db
from app.routes import auth, protected


# Create FastAPI app
app = FastAPI(
    title="Caravane Restaurant Management API",
    description="JWT Authentication with Role-Based Access Control",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for better error responses."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.ENVIRONMENT == "development" else "Something went wrong"
        }
    )


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    try:
        await connect_db()
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    try:
        await disconnect_db()
        print("✅ Database disconnected successfully")
    except Exception as e:
        print(f"❌ Error disconnecting from database: {e}")


# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(protected.router, prefix="/api")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Caravane API is running",
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Caravane Restaurant Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
