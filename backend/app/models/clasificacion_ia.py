import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.config import Base


class ClasificacionIAModel(Base):
    __tablename__ = "clasificaciones_ia"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reporte_id: Mapped[str] = mapped_column(String(36), ForeignKey("reportes.id"), nullable=False, unique=True)
    severidad: Mapped[str] = mapped_column(String(20), nullable=False)
    confianza: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    justificacion: Mapped[str] = mapped_column(Text, nullable=False)
    coincide_tipo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    reporte = relationship("ReporteModel", back_populates="clasificacion_ia")
