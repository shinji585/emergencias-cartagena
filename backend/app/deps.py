from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.config import get_db
from app.services.usuario import UsuarioService
from app.services.reporte import ReporteService
from app.services.operador import OperadorService


def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioService:
    return UsuarioService(db)


def get_reporte_service(db: Session = Depends(get_db)) -> ReporteService:
    return ReporteService(db)


def get_operador_service(db: Session = Depends(get_db)) -> OperadorService:
    return OperadorService(db)
