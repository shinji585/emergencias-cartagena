from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from app.core.logging.logger import logger
from app.db.config import Base, engine
from app.models import ClasificacionIAModel, ReporteModel, UsuarioModel  # noqa: F401
from app.routers import health_router, operador_router, reporte_router, usuario_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Iniciando API y creando tablas de base de datos si no existen...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas inicializadas correctamente.")
    yield
    # Shutdown


app = FastAPI(
    title="API Sistema de Emergencias Cartagena",
    description="Backend para el reporte de emergencias con trazabilidad legal e IA (Ollama)",
    version="1.0.0",
    lifespan=lifespan,
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



@app.get("/scalar", include_in_schema=False)
async def scalar_html() -> HTMLResponse:
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Tracked product Documentation Scalar")