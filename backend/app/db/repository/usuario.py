from sqlalchemy.orm import Session

from app.db.repository.base import BaseRepository
from app.models.usuario import UsuarioModel


class UsuarioRepository(BaseRepository[UsuarioModel]):
    def __init__(self, db: Session):
        super().__init__(UsuarioModel, db)

    def get_by_telefono(self, telefono: str) -> UsuarioModel | None:
        return (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.telefono == telefono)
            .first()
        )
