from datetime import datetime
from pydantic import ConfigDict, Field
from app.schemas.enums import Severidad, EstadoReporte
from app.schemas.reporte.base import ReporteBase


class ReportePublic(ReporteBase):
    id: str = Field(..., description="ID del reporte")
    usuario_id: str = Field(..., description="ID del usuario")
    severidad: Severidad = Field(..., description="Severidad determinada")
    estado: EstadoReporte = Field(..., description="Estado actual")
    resumen_ia: str | None = Field(default=None, description="Resumen generado por la IA")
    grupo_incidente_id: str | None = Field(default=None, description="ID del incidente duplicado o agrupado")
    created_at: datetime = Field(..., description="Timestamp de creación")
    updated_at: datetime | None = Field(default=None, description="Timestamp de actualización")

    model_config = ConfigDict(from_attributes=True)
