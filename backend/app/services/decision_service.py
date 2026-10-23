from app.repositories.decision_repository import registrar_decision
from app.repositories.solicitud_repository import obtener_solicitud_por_id

# Estados en los que se puede aprobar o rechazar una solicitud.
# Ajustar cuando US-018 (evaluar solicitud) defina su estado final.
ESTADOS_DECIDIBLES = ["enviada"]

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
