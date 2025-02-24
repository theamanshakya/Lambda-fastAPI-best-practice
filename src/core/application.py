from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ..config import get_settings
from ..routes import user_routes
from .middleware import request_middleware
from .exceptions import CustomHTTPException
import logging

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    settings = get_settings()
    
    app = FastAPI(
        title="User API",
        description="FastAPI Snowflake Lambda Architecture",
        version="1.0.0",
        docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc"
    )
    
    # Middleware
    app.middleware("http")(request_middleware)
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Error handling
    @app.exception_handler(CustomHTTPException)
    async def custom_exception_handler(request: Request, exc: CustomHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "code": exc.error_code,
                "extra": exc.extra
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "code": "INTERNAL_ERROR"
            }
        )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    # Routes
    app.include_router(
        user_routes.router,
        prefix=settings.API_V1_PREFIX
    )
    
    return app 