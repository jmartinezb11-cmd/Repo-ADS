from fastapi import APIRouter
from app.schemas.comite_schema import ComiteResponse
from app.services.comite_service import consultar_comite_real
from fastapi import Depends, HTTPException, status
from app.core.deps import require_role
from app.core.roles import Role
from app.schemas.comite_schema import CrearComiteRequest, CrearComiteResponse
from app.services.comite_service import crear_comite
from app.schemas.comite_schema import (
    AsignarMiembroRequest,
    AsignarMiembroResponse
)
from app.services.comite_service import asignar_miembro_comite

router = APIRouter(prefix="/comite", tags=["US-023 - Comité"])


@router.get("/{id_comite}", response_model=ComiteResponse)
def consultar_comite(id_comite: int):
    try:
        return consultar_comite_real(id_comite)

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

def registrar_comite(
    datos: CrearComiteRequest,
    usuario_actual: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        return crear_comite(
            nombre_comite=datos.nombre_comite,
            descripcion=datos.descripcion
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post(
    "/{id_comite}/miembros",
    response_model=AsignarMiembroResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_miembro_comite(
    id_comite: int,
    datos: AsignarMiembroRequest,
    usuario_actual: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        return asignar_miembro_comite(
            id_comite=id_comite,
            id_estudiante=datos.id_estudiante,
            rol_comite=datos.rol_comite
        )

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
