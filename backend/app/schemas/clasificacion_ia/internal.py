import uuid
from datetime import UTC, datetime

from pydantic import Field

from app.schemas.clasificacion_ia.create import ClasificacionIACreate


class ClasificacionIAInternal(ClasificacionIACreate):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="ID único del análisis de IA",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp de clasificación",
    )
