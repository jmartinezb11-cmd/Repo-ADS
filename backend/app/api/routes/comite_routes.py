from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import require_role
from app.core.roles import Role
from app.schemas.comite_schema import (
    ComiteResponse,
    CrearComiteRequest,
    CrearComiteResponse,
    AsignarMiembroRequest,
    AsignarMiembroResponse,
)
from app.services.comite_service import (
    consultar_comite_real,
    crear_comite,
    asignar_miembro_comite,
    listar_comites,
)

router = APIRouter(prefix="/comite", tags=["US-023 - Comité"])


@router.get("")
def obtener_comites(
    usuario_actual: dict = Depends(
        require_role(Role.ADMINISTRADOR)
    )
):
    return {
        "comites": listar_comites()
    }


@router.get("/{id_comite}", response_model=ComiteResponse)
def consultar_comite(id_comite: int):
    """
    US-023: Consultar integrantes de un comité y sus asignaciones.
    """
    try:
        return consultar_comite_real(id_comite)
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.post(
    "",
    response_model=CrearComiteResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_comite(
    datos: CrearComiteRequest,
    usuario_actual: dict = Depends(require_role(Role.ADMINISTRADOR)),
):
    """
    US-023: Registrar un nuevo comité.
    """
    try:
        return crear_comite(
            nombre_comite=datos.nombre_comite,
            descripcion=datos.descripcion,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.post(
    "/{id_comite}/miembros",
    response_model=AsignarMiembroResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_miembro_comite(
    id_comite: int,
    datos: AsignarMiembroRequest,
    usuario_actual: dict = Depends(require_role(Role.ADMINISTRADOR)),
):
    """
    US-023: Asignar integrante a un comité.
    """
    try:
        return asignar_miembro_comite(
            id_comite=id_comite,
            id_estudiante=datos.id_estudiante,
            rol_comite=datos.rol_comite,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),

        )
    
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )