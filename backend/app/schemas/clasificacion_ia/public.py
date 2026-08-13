from datetime import datetime

from pydantic import ConfigDict, Field

from app.schemas.clasificacion_ia.base import ClasificacionIABase


class ClasificacionIAPublic(ClasificacionIABase):
    id: str = Field(..., description="ID de la clasificación")
    reporte_id: str = Field(..., description="ID del reporte")
    created_at: datetime = Field(..., description="Fecha de creación")

    model_config = ConfigDict(from_attributes=True)
