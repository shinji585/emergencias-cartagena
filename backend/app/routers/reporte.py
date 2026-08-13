from fastapi import APIRouter, Depends, status
from app.deps import get_reporte_service
from app.schemas.reporte.create import ReporteCreate
from app.schemas.reporte.public import ReportePublic
from app.services.reporte import ReporteService

router = APIRouter(prefix="/api/v1/reportes", tags=["Reportes"])


@router.post("", response_model=ReportePublic, status_code=status.HTTP_201_CREATED)
async def crear_reporte(
    payload: ReporteCreate,
    service: ReporteService = Depends(get_reporte_service)
):
    return await service.crear_reporte(payload)


@router.get("/usuario/{usuario_id}", response_model=list[ReportePublic])
def obtener_historial_usuario(
    usuario_id: str,
    service: ReporteService = Depends(get_reporte_service)
):
    return service.obtener_historial_usuario(usuario_id)
