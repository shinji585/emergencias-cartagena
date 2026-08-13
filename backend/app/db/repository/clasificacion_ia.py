from sqlalchemy.orm import Session
from app.db.repository.base import BaseRepository
from app.models.clasificacion_ia import ClasificacionIAModel


class ClasificacionIARepository(BaseRepository[ClasificacionIAModel]):
    def __init__(self, db: Session):
        super().__init__(ClasificacionIAModel, db)

    def get_by_reporte_id(self, reporte_id: str) -> ClasificacionIAModel | None:
        return (
            self.db.query(ClasificacionIAModel)
            .filter(ClasificacionIAModel.reporte_id == reporte_id)
            .first()
        )
