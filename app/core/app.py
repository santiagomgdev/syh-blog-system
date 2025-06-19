from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config.settings import settings
from app.modules.router.v1.router import router
from app.modules.router.oauth.router import router as oauth_router
# from app.core.database import create_tables

def create_app() -> FastAPI:

    # Inicializa tablas BD
    # create_tables()

    # Crea Instancia de FastAPI
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        description="Una plataforma de blogs moderna construida con FastAPI"
    )
    
    # Rutas iniciales
    setup_routes(app)
    
    return app

def setup_routes(app: FastAPI) -> None:

    app.include_router(oauth_router, prefix="/api/v1")
    app.include_router(router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {
            "message": f"Bienvenido a {settings.APP_NAME}",
            "version": settings.VERSION,
            "status": "en ejecución"
        }
    
    @app.get("/health")
    async def health_check():
        """Punto de comprobación de salud"""
        return {"status": "saludable"}
