from pydantic import Field

from app.schemas.reporte.base import ReporteBase


class ReporteCreate(ReporteBase):
    usuario_id: str | None = Field(
        default=None, description="ID del usuario si ya está registrado"
    )
    usuario_nombre: str | None = Field(
        default=None, description="Nombre del usuario en caso de registro rápido"
    )
    usuario_telefono: str | None = Field(
        default=None, description="Teléfono del usuario en caso de registro rápido"
    )
