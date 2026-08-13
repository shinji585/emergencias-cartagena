import uuid
from datetime import datetime, timezone
from pydantic import Field
from app.schemas.usuario.create import UsuarioCreate


class UsuarioInternal(UsuarioCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="ID único del usuario")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Fecha de registro")
