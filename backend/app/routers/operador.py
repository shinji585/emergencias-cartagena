from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_operador_service
from app.schemas.enums import EstadoReporte
from app.schemas.reporte.public import ReportePublic
from app.services.operador import OperadorService

router = APIRouter(prefix="/api/v1/operador", tags=["Operador Dashboard"])


@router.get("/cola")
def obtener_cola_priorizada(service: OperadorService = Depends(get_operador_service)):
    return service.obtener_cola_priorizada()


@router.patch("/reportes/{reporte_id}/estado", response_model=ReportePublic)
def actualizar_estado_reporte(
    reporte_id: str,
    nuevo_estado: EstadoReporte,
    service: OperadorService = Depends(get_operador_service),
):
    if not reporte_id or not reporte_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="reporte_id es requerido",
        )
    actualizado = service.actualizar_estado(reporte_id, nuevo_estado)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado"
        )
    return actualizado


@router.get("/metricas")
def obtener_metricas(service: OperadorService = Depends(get_operador_service)):
    return service.obtener_metricas()
