from sqlalchemy.orm import Session

from app.core.logging.logger import logger
from app.db.repository.usuario import UsuarioRepository
from app.schemas.usuario.create import UsuarioCreate
from app.schemas.usuario.internal import UsuarioInternal
from app.schemas.usuario.public import UsuarioPublic


class UsuarioService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def registrar_o_buscar(self, payload: UsuarioCreate) -> UsuarioPublic:
        existente = self.repository.get_by_telefono(payload.telefono)
        if existente:
            logger.info(f"Usuario existente encontrado con teléfono {payload.telefono}")
            return UsuarioPublic.model_validate(existente)

        internal = UsuarioInternal(**payload.model_dump())
        nuevo = self.repository.create(internal.model_dump())
        logger.info(f"Nuevo usuario registrado con ID {nuevo.id}")
        return UsuarioPublic.model_validate(nuevo)

    def obtener_por_id(self, usuario_id: str) -> UsuarioPublic | None:
        user = self.repository.get_by_id(usuario_id)
        if not user:
            return None
        return UsuarioPublic.model_validate(user)
