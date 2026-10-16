from app.models.evaluacion import Evaluacion
from app.repositories.estudiante_repository import obtener_estudiante_por_id
from app.repositories.evaluacion_repository import (
    crear_evaluacion,
    obtener_evaluacion_por_id,
    existe_evaluacion,
    listar_evaluaciones_por_evaluador,
    listar_solicitudes_por_estados,
    listar_evaluadores_activos,
    obtener_resumen_solicitud,
    registrar_resultado_evaluacion,
)
from app.repositories.solicitud_repository import (
    obtener_solicitud_por_id,
    obtener_detalle_solicitud,
)

# Estados de solicitud en los que se permite asignar un evaluador.
ESTADOS_ASIGNABLES = ["pendiente", "enviada"]


# US-017 - Asignar evaluación

def asignar_evaluacion(
    id_solicitud: int,
    id_evaluador: int,
    id_asignador: int
) -> dict:

    solicitud = obtener_solicitud_por_id(id_solicitud)

    if solicitud is None:
        raise ValueError("La solicitud no existe.")

    if solicitud["estado"] not in ESTADOS_ASIGNABLES:
        raise ValueError(
            f"No se puede asignar una solicitud en estado "
            f"'{solicitud['estado']}'."
        )

    evaluador = obtener_estudiante_por_id(id_evaluador)

    if evaluador is None:
        raise ValueError("El evaluador no existe.")

    if evaluador["rol"] != "evaluador":
        raise ValueError("El usuario indicado no tiene rol de evaluador.")

    if evaluador["estado_cuenta"] == "inactivo":
        raise ValueError("La cuenta del evaluador está inactiva.")

    if solicitud["id_estudiante"] == id_evaluador:
        raise ValueError(
            "Un evaluador no puede evaluar su propia solicitud."
        )

    if existe_evaluacion(id_solicitud, id_evaluador):
        raise ValueError(
            "Esta solicitud ya está asignada a ese evaluador."
        )

    evaluacion = Evaluacion(
        id_solicitud=id_solicitud,
        id_evaluador=id_evaluador,
        id_asignador=id_asignador,
    )

    id_evaluacion = crear_evaluacion(evaluacion)

    return obtener_evaluacion_por_id(id_evaluacion)


def obtener_asignaciones_de_evaluador(id_evaluador: int) -> list[dict]:
    return listar_evaluaciones_por_evaluador(id_evaluador)


def obtener_solicitudes_asignables() -> list[dict]:
    return listar_solicitudes_por_estados(ESTADOS_ASIGNABLES)


def obtener_evaluadores_disponibles() -> list[dict]:
    return listar_evaluadores_activos()


# US-018 - Evaluar solicitud

def obtener_detalle_evaluacion(
    id_evaluacion: int,
    id_evaluador: int | None
) -> dict:
    # id_evaluador es None cuando consulta un administrador.
    evaluacion = obtener_evaluacion_por_id(id_evaluacion)

    if evaluacion is None:
        raise ValueError("La evaluación no existe.")

    if id_evaluador is not None and evaluacion["id_evaluador"] != id_evaluador:
        raise PermissionError("Esta evaluación no está asignada a ti.")

    return {
        "evaluacion": evaluacion,
        "solicitud": obtener_resumen_solicitud(evaluacion["id_solicitud"]),
        "detalle": obtener_detalle_solicitud(evaluacion["id_solicitud"]),
    }


def evaluar_solicitud(
    id_evaluacion: int,
    id_evaluador: int,
    puntaje: int,
    recomendacion: str
) -> dict:

    evaluacion = obtener_evaluacion_por_id(id_evaluacion)

    if evaluacion is None:
        raise ValueError("La evaluación no existe.")

    if evaluacion["id_evaluador"] != id_evaluador:
        raise PermissionError("Esta evaluación no está asignada a ti.")

    if evaluacion["estado"] != "asignada":
        raise ValueError(
            "Esta evaluación ya fue registrada y no se puede modificar."
        )

    registrada = registrar_resultado_evaluacion(
        id_evaluacion=id_evaluacion,
        puntaje=puntaje,
        recomendacion=recomendacion,
    )

    if not registrada:
        raise ValueError(
            "Esta evaluación ya fue registrada y no se puede modificar."
        )

    return obtener_evaluacion_por_id(id_evaluacion)