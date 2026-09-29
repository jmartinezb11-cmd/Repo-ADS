from fastapi import APIRouter, HTTPException, Depends

from app.core.deps import require_role
from app.core.roles import Role

from app.schemas.usuario import (
    ListaUsuariosResponse,
    UsuarioResumen,
    CambiarEstadoRequest,
    CambiarEstadoResponse
)

from app.services.usuario_service import (
    obtener_lista_usuarios,
    obtener_usuario,
    cambiar_estado_usuario
)


router = APIRouter(
    prefix="/api/usuarios",
    tags=["Gestión de usuarios"]
)


@router.get("/", response_model=ListaUsuariosResponse)
def listar(
    usuario_actual: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    usuarios = obtener_lista_usuarios()

    return {"usuarios": usuarios}


@router.get("/{id_estudiante}", response_model=UsuarioResumen)
def obtener(
    id_estudiante: int,
    usuario_actual: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        return obtener_usuario(id_estudiante)

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.patch("/{id_estudiante}/estado", response_model=CambiarEstadoResponse)
def cambiar_estado(
    id_estudiante: int,
    data: CambiarEstadoRequest,
    usuario_actual: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        resultado = cambiar_estado_usuario(
            id_estudiante=id_estudiante,
            nuevo_estado=data.nuevo_estado,
            usuario_actual=usuario_actual
        )

        return {
            "mensaje": "Estado actualizado correctamente",
            "id_estudiante": resultado["id_estudiante"],
            "nuevo_estado": resultado["nuevo_estado"]
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))