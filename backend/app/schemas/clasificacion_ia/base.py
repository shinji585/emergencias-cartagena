from pydantic import BaseModel, Field
from app.schemas.enums import Severidad


class ClasificacionIABase(BaseModel):
    severidad: Severidad = Field(..., description="Severidad determinada por el modelo de visión")
    confianza: float = Field(default=0.85, description="Nivel de confianza entre 0.0 y 1.0")
    justificacion: str = Field(..., description="Justificación en una sola línea del análisis de la foto")
    coincide_tipo: bool = Field(default=True, description="Si la foto concuerda con el tipo de emergencia")
