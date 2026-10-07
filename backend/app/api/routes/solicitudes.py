from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import require_role, get_current_user
from app.core.roles import Role
from app.services.solicitud_service import (
    registrar_solicitud,
    completar_solicitud,
    consultar_solicitudes_estudiante,
    consultar_solicitud,
)

from app.schemas.solicitud import CompletarSolicitudRequest

router = APIRouter(
    prefix="/api/solicitudes",
    tags=["Solicitudes"]
)


# US-010 - Crear solicitud

@router.post("/convocatoria/{id_convocatoria}", status_code=201)
def crear(
    id_convocatoria: int,
    user: dict = Depends(require_role(Role.ESTUDIANTE))
):
    try:
        solicitud = registrar_solicitud(
            id_estudiante=user["id"],
            id_convocatoria=id_convocatoria
        )

        return {
            "mensaje": "Solicitud creada correctamente",
            "solicitud": solicitud
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al crear la solicitud."
        )

# US-011 - Completar solicitud

@router.put("/{id_solicitud}/completar")
def completar(
    id_solicitud: int,
    datos: CompletarSolicitudRequest,
    user: dict = Depends(require_role(Role.ESTUDIANTE))
):
    try:
        detalle = completar_solicitud(
            id_solicitud=id_solicitud,
            id_estudiante=user["id"],
            datos=datos
        )

        return {
            "mensaje": "Solicitud completada correctamente",
            "detalle": detalle
        }

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al completar la solicitud."
        )

    # US-013 - Consultar solicitudes

@router.get("/mis-solicitudes")
def listar_mis_solicitudes(
    user: dict = Depends(require_role(Role.ESTUDIANTE))
):
    try:
        solicitudes = consultar_solicitudes_estudiante(
            id_estudiante=user["id"]
        )

        return {
            "solicitudes": solicitudes
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar las solicitudes."
        )


@router.get("/{id_solicitud}")
def obtener_mi_solicitud(
    id_solicitud: int,
    user: dict = Depends(require_role(Role.ESTUDIANTE))
):
    try:
        return consultar_solicitud(
            id_solicitud=id_solicitud,
            id_estudiante=user["id"]
        )

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar la solicitud."
        )