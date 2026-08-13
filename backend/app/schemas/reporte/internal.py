import uuid
from datetime import datetime, timezone
from pydantic import Field
from app.schemas.enums import Severidad, EstadoReporte
from app.schemas.reporte.create import ReporteCreate


class ReporteInternal(ReporteCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="ID único del reporte")
    usuario_id: str = Field(..., description="ID del usuario asignado")
    severidad: Severidad = Field(default=Severidad.MODERADO, description="Severidad determinada por IA")
    estado: EstadoReporte = Field(default=EstadoReporte.PENDIENTE, description="Estado del reporte")
    resumen_ia: str | None = Field(default=None, description="Resumen descriptivo generado por la IA")
    grupo_incidente_id: str | None = Field(default=None, description="ID del grupo de incidentes similares")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp de creación")
    updated_at: datetime | None = Field(default=None, description="Timestamp de actualización")
