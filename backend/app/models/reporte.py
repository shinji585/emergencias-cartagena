import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.config import Base


class ReporteModel(Base):
    __tablename__ = "reportes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    tipo_emergencia: Mapped[str] = mapped_column(String(50), nullable=False)
    ubicacion_lat: Mapped[float] = mapped_column(Float, nullable=False)
    ubicacion_lng: Mapped[float] = mapped_column(Float, nullable=False)
    foto_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    severidad: Mapped[str] = mapped_column(String(20), default="moderado")
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    organismo: Mapped[str] = mapped_column(String(30), nullable=False)
    usuario_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("usuarios.id"), nullable=False
    )
    resumen_ia: Mapped[str | None] = mapped_column(Text, nullable=True)
    grupo_incidente_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=lambda: datetime.now(UTC), nullable=True
    )

    usuario = relationship("UsuarioModel", back_populates="reportes")
    clasificacion_ia = relationship(
        "ClasificacionIAModel",
        back_populates="reporte",
        uselist=False,
        cascade="all, delete-orphan",
    )
