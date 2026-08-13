from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.db.repository.base import BaseRepository
from app.models.reporte import ReporteModel


class ReporteRepository(BaseRepository[ReporteModel]):
    def __init__(self, db: Session):
        super().__init__(ReporteModel, db)

    def get_by_usuario(self, usuario_id: str) -> Sequence[ReporteModel]:
        return (
            self.db.query(ReporteModel)
            .filter(ReporteModel.usuario_id == usuario_id)
            .order_by(ReporteModel.created_at.desc())
            .all()
        )

    def get_cola_operador(self) -> Sequence[ReporteModel]:
        return (
            self.db.query(ReporteModel)
            .filter(
                ReporteModel.estado != "resuelto", ReporteModel.estado != "descartado"
            )
            .order_by(ReporteModel.created_at.asc())
            .all()
        )
