from app.repositories.decision_repository import (
    registrar_decision,
    obtener_resumen_evaluaciones,
)
from app.repositories.solicitud_repository import obtener_solicitud_por_id

# Estados en los que se puede aprobar o rechazar una solicitud.
# La evaluación (US-018) no cambia el estado de la solicitud.
ESTADOS_DECIDIBLES = ["enviada"]

# Estado que deja US-018 en una evaluación ya registrada.
ESTADO_EVALUACION_TERMINADA = "evaluada"

DECISIONES = ("aprobada", "rechazada")


class SolicitudNoEncontrada(Exception):
    pass


# US-024 - Aprobar o rechazar solicitud

def procesar_decision(
    id_solicitud: int,
    decision: str,
    comentario: str | None,
    id_decisor: int
) -> dict:

    if decision not in DECISIONES:
        raise ValueError("La decisión debe ser 'aprobada' o 'rechazada'.")

    comentario = (comentario or "").strip() or None

    if decision == "rechazada" and comentario is None:
        raise ValueError("Debes indicar el motivo del rechazo.")

    solicitud = obtener_solicitud_por_id(id_solicitud)

    if solicitud is None:
        raise SolicitudNoEncontrada("Solicitud no encontrada.")

    if solicitud["estado"] in DECISIONES:
        raise ValueError(
            f"Esta solicitud ya fue resuelta "
            f"(estado actual: '{solicitud['estado']}')."
        )

    if solicitud["estado"] not in ESTADOS_DECIDIBLES:
        raise ValueError(
            f"No se puede decidir una solicitud en estado "
            f"'{solicitud['estado']}'. Debe estar en: "
            f"{', '.join(ESTADOS_DECIDIBLES)}."
        )

    resumen = obtener_resumen_evaluaciones(
        id_solicitud,
        ESTADO_EVALUACION_TERMINADA
    )

    if resumen["total"] == 0:
        raise ValueError(
            "La solicitud todavía no tiene evaluaciones asignadas."
        )

    if resumen["evaluadas"] < resumen["total"]:
        pendientes = resumen["total"] - resumen["evaluadas"]
        raise ValueError(
            f"Todavía hay {pendientes} evaluación(es) pendiente(s) "
            f"de registrar."
        )

    resultado = registrar_decision(
        id_solicitud,
        decision,
        comentario,
        id_decisor,
        ESTADOS_DECIDIBLES
    )

    if resultado is None:
        raise ValueError(
            "La solicitud cambió de estado mientras se procesaba. "
            "Inténtalo de nuevo."
        )

    return resultado
