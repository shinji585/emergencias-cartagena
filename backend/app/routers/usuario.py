from fastapi import APIRouter, Depends, HTTPException, status
from app.deps import get_usuario_service
from app.schemas.usuario.create import UsuarioCreate
from app.schemas.usuario.public import UsuarioPublic
from app.services.usuario import UsuarioService

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])


@router.post("", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    payload: UsuarioCreate,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.registrar_o_buscar(payload)


@router.get("/{usuario_id}", response_model=UsuarioPublic)
def obtener_usuario(
    usuario_id: str,
    service: UsuarioService = Depends(get_usuario_service)
):
    usuario = service.obtener_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario
