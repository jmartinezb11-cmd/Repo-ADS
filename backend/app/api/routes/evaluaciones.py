import logging
from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import require_role
from app.core.roles import Role
from app.schemas.evaluacion import (
    AsignarEvaluacionRequest,
    EvaluacionRespuesta,
    AsignacionEvaluador,
    SolicitudAsignable,
    EvaluadorDisponible,
    EvaluarSolicitudRequest,
    EvaluacionDetalle,
)
from app.services.evaluacion_service import (
    asignar_evaluacion,
    obtener_asignaciones_de_evaluador,
    obtener_solicitudes_asignables,
    obtener_evaluadores_disponibles,
    obtener_detalle_evaluacion,
    evaluar_solicitud,
)
logger = logging.getLogger(__name__)

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
        logger.exception("Error inesperado al asignar evaluación")
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


# US-018 - Evaluar solicitud
# IMPORTANTE: estas rutas con {id_evaluacion} van al final, después de
# las rutas fijas (/mis-asignaciones, /solicitudes, /evaluadores).
# Si fueran antes, FastAPI confundiría esos textos con un id.

@router.get(
    "/{id_evaluacion}",
    response_model=EvaluacionDetalle
)
def consultar_evaluacion(
    id_evaluacion: int,
    user: dict = Depends(require_role(Role.EVALUADOR, Role.ADMINISTRADOR))
):
    try:
        id_evaluador = user["id"] if user["rol"] == Role.EVALUADOR else None

        return obtener_detalle_evaluacion(
            id_evaluacion=id_evaluacion,
            id_evaluador=id_evaluador
        )

    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar la evaluación."
        )


@router.put(
    "/{id_evaluacion}/evaluar",
    response_model=EvaluacionRespuesta
)
def evaluar(
    id_evaluacion: int,
    datos: EvaluarSolicitudRequest,
    user: dict = Depends(require_role(Role.EVALUADOR))
):
    try:
        return evaluar_solicitud(
            id_evaluacion=id_evaluacion,
            id_evaluador=user["id"],
            puntaje=datos.puntaje,
            recomendacion=datos.recomendacion
        )

    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al registrar la evaluación."
        )