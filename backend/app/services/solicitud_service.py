from app.models.solicitud import Solicitud
from app.repositories.solicitud_repository import (
    crear_solicitud,
    obtener_solicitud_por_id,
    existe_solicitud_duplicada,
)
from app.repositories.convocatoria_repository import obtener_convocatoria_por_id


def registrar_solicitud(id_estudiante: int, id_convocatoria: int) -> dict:
    convocatoria = obtener_convocatoria_por_id(id_convocatoria)

    if convocatoria is None:
        raise ValueError("Convocatoria no encontrada.")

    if convocatoria["estado"] != "publicada":
        raise ValueError(
            f"No se puede solicitar: la convocatoria está en estado "
            f"'{convocatoria['estado']}', debe estar 'publicada'."
        )

    if existe_solicitud_duplicada(id_estudiante, id_convocatoria):
        raise ValueError(
            "Ya existe una solicitud de este estudiante para esta convocatoria."
        )

    solicitud = Solicitud(
        id_estudiante=id_estudiante,
        id_convocatoria=id_convocatoria,
    )

    id_solicitud = crear_solicitud(solicitud)

    return obtener_solicitud_por_id(id_solicitud)
