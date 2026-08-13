from pydantic import Field
from app.schemas.clasificacion_ia.base import ClasificacionIABase


class ClasificacionIACreate(ClasificacionIABase):
    reporte_id: str = Field(..., description="ID del reporte asociado")
