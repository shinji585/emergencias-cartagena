from datetime import datetime
from pydantic import ConfigDict, Field
from app.schemas.usuario.base import UsuarioBase


class UsuarioPublic(UsuarioBase):
    id: str = Field(..., description="ID del usuario")
    created_at: datetime = Field(..., description="Fecha de creación")

    model_config = ConfigDict(from_attributes=True)
