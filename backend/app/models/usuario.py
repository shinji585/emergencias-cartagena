import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.config import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    identificacion: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    reportes = relationship("ReporteModel", back_populates="usuario", cascade="all, delete-orphan")
