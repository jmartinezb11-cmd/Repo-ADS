from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import require_role
from app.core.roles import Role
from app.schemas.evaluacion import (
    AsignarEvaluacionRequest,
    EvaluacionRespuesta,
    AsignacionEvaluador,
    SolicitudAsignable,
    EvaluadorDisponible,
)
from app.services.evaluacion_service import (
    asignar_evaluacion,
    obtener_asignaciones_de_evaluador,
    obtener_solicitudes_asignables,
    obtener_evaluadores_disponibles,
)

router = APIRouter(
    prefix="/api/evaluaciones",
    tags=["Evaluaciones"]
)


# US-017 - Asignar evaluación

@router.post(
    "",
    response_model=EvaluacionRespuesta,
    status_code=201
)
def asignar(
    datos: AsignarEvaluacionRequest,
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        return asignar_evaluacion(
            id_solicitud=datos.id_solicitud,
            id_evaluador=datos.id_evaluador,
            id_asignador=user["id"]
        )

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al asignar la evaluación."
        )


@router.get(
    "/mis-asignaciones",
    response_model=list[AsignacionEvaluador]
)
def mis_asignaciones(
    user: dict = Depends(require_role(Role.EVALUADOR))
):
    try:
        return obtener_asignaciones_de_evaluador(user["id"])

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar las asignaciones."
        )


# Datos para la pantalla de asignación (solo administrador)

@router.get(
    "/solicitudes",
    response_model=list[SolicitudAsignable]
)
def solicitudes_asignables(
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        return obtener_solicitudes_asignables()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar las solicitudes."
        )


@router.get(
    "/evaluadores",
    response_model=list[EvaluadorDisponible]
)
def evaluadores_disponibles(
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        return obtener_evaluadores_disponibles()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar los evaluadores."
        )