from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.config import Base, engine
from app.models import UsuarioModel, ReporteModel, ClasificacionIAModel  # noqa: F401
from app.routers import health_router, usuario_router, reporte_router, operador_router
from app.core.logging.logger import logger

app = FastAPI(
    title="API Sistema de Emergencias Cartagena",
    description="Backend para el reporte de emergencias con trazabilidad legal e IA (Ollama)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(usuario_router)
app.include_router(reporte_router)
app.include_router(operador_router)


@app.on_event("startup")
def startup_event():
    logger.info("Iniciando API y creando tablas de base de datos si no existen...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas inicializadas correctamente.")
