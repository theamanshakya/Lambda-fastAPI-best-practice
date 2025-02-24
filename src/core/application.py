from fastapi import FastAPI
from src.modules.users.controller import router as user_router
from .middleware import request_middleware
from src.utils.logger import setup_logger

def create_app() -> FastAPI:
    # Setup logging
    setup_logger()
    
    app = FastAPI(title="API")
    
    # Add middleware
    app.middleware("http")(request_middleware)
    
    # Register routes
    app.include_router(user_router, prefix="/api/v1")
    
    return app 