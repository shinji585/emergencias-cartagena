from pydantic import BaseModel, Field


class UsuarioBase(BaseModel):
    nombre: str = Field(..., description="Nombre completo del ciudadano")
    telefono: str = Field(
        ..., description="Número de teléfono de contacto para trazabilidad"
    )
    identificacion: str | None = Field(
        default=None, description="Cédula / Documento de identidad opcional"
    )
