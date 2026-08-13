from app.routers.health import router as health_router
from app.routers.usuario import router as usuario_router
from app.routers.reporte import router as reporte_router
from app.routers.operador import router as operador_router

__all__ = ["health_router", "usuario_router", "reporte_router", "operador_router"]
