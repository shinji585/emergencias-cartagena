from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_reporte_service
from app.schemas.reporte.create import ReporteCreate
from app.schemas.reporte.despacho import DespachoResponse
from app.schemas.reporte.public import ReportePublic
from app.services.reporte import ReporteService

router = APIRouter(prefix="/api/v1/reportes", tags=["Reportes"])


@router.post("", response_model=ReportePublic, status_code=status.HTTP_201_CREATED)
async def crear_reporte(
    payload: ReporteCreate, service:  Annotated[ ReporteService,Depends(get_reporte_service)]
):
    """
    Crea un nuevo reporte de emergencia.
    
    - Integra análisis de visión (si hay imagen) + texto (Ollama)
    - Detecta HAZMAT, desastres, zona insular, Plan Candado
    - Enruta automáticamente a organismos correspondientes
    """
    try:
        return await service.crear_reporte(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el reporte: {e!s}",
        )


@router.get("/{reporte_id}", response_model=ReportePublic)
def obtener_reporte(
    reporte_id: str, service: Annotated[ReporteService, Depends(get_reporte_service)]
):
    """
    Obtiene un reporte específico por su ID.
    
    Retorna:
    - ID del reporte
    - Tipo de emergencia y severidad
    - Ubicación GPS
    - Análisis IA (clasificación)
    - Usuario que reportó
    """
    if not reporte_id or not reporte_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="reporte_id es requerido",
        )
    
    reporte = service.obtener_reporte_por_id(reporte_id)
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte {reporte_id} no encontrado",
        )
    return reporte


@router.get("/{reporte_id}/despacho", response_model=DespachoResponse)
def obtener_despacho_reporte(
    reporte_id: str, service: Annotated[ReporteService, Depends(get_reporte_service)]
):
    """
    Genera despacho operativo para un reporte.
    
    Ejecuta:
    - Análisis de modelos Ollama (visión + orquestación)
    - Detección de casos especiales (HAZMAT, desastre, insular)
    - Enrutamiento inteligente a organismos
    - Plan Candado para robos/inseguridad
    
    Responde con lista de organismos a despachar y acciones.
    """
    if not reporte_id or not reporte_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="reporte_id es requerido",
        )
    
    despacho = service.generar_despacho(reporte_id, actualizar_estado=False)
    if not despacho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte {reporte_id} no encontrado o sin análisis disponible",
        )
    return despacho


@router.get("/usuario/{usuario_id}", response_model=list[ReportePublic])
def obtener_historial_usuario(
    usuario_id: str, service: Annotated[ReporteService, Depends(get_reporte_service)]
):
    """
    Obtiene historial de reportes de un usuario específico.
    """
    if not usuario_id or not usuario_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="usuario_id es requerido",
        )
    return service.obtener_historial_usuario(usuario_id)
