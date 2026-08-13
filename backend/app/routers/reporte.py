from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_reporte_service
from app.schemas.reporte.create import ReporteCreate
from app.schemas.reporte.public import ReportePublic
from app.services.reporte import ReporteService

router = APIRouter(prefix="/api/v1/reportes", tags=["Reportes"])


@router.post("", response_model=ReportePublic, status_code=status.HTTP_201_CREATED)
async def crear_reporte(
    payload: ReporteCreate, service: ReporteService = Depends(get_reporte_service)
):
    try:
        return await service.crear_reporte(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar el reporte",
        )


@router.get("/usuario/{usuario_id}", response_model=list[ReportePublic])
def obtener_historial_usuario(
    usuario_id: str, service: ReporteService = Depends(get_reporte_service)
):
    if not usuario_id or not usuario_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="usuario_id es requerido",
        )
    return service.obtener_historial_usuario(usuario_id)
