from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.core.config import settings
from app.core.logger import setup_logging
from app.db.session import engine, Base

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/api/docs",
        redoc_url=None
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    setup_logging()
    
    app.include_router(api_router, prefix="/api/v1")
    
    @app.on_event("startup")
    def startup():
        Base.metadata.create_all(bind=engine)
    
    @app.get("/health")
    def health_check():
        return {"status": "ok"}
    
    return app

app = create_app()