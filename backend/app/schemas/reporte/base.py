from pydantic import BaseModel, Field

from app.schemas.enums import Organismo, TipoEmergencia


class ReporteBase(BaseModel):
    tipo_emergencia: TipoEmergencia = Field(
        ..., description="Tipo de emergencia reportada"
    )
    ubicacion_lat: float = Field(..., description="Latitud de la ubicación GPS")
    ubicacion_lng: float = Field(..., description="Longitud de la ubicación GPS")
    foto_url: str | None = Field(
        default=None, description="URL o base64 de la foto capturada"
    )
    descripcion: str | None = Field(
        default=None, description="Descripción detallada de la emergencia"
    )
    organismo: Organismo = Field(
        ..., description="Organismo asignado para atender la emergencia"
    )
