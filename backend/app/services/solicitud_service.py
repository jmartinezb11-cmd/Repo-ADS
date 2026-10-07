from app.models.solicitud import Solicitud
from app.models.detalle_solicitud import DetalleSolicitud

from app.repositories.solicitud_repository import (
    crear_solicitud,
    obtener_solicitud_por_id,
    existe_solicitud_duplicada,
    guardar_detalle_solicitud,
    obtener_detalle_solicitud,
    obtener_solicitudes_por_estudiante,
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

# US-011 - Completar solicitud

def completar_solicitud(
    id_solicitud: int,
    id_estudiante: int,
    datos
) -> dict:
    solicitud = obtener_solicitud_por_id(id_solicitud)

    # La solicitud debe existir.
    if solicitud is None:
        raise ValueError("Solicitud no encontrada.")

    # El estudiante solo puede modificar sus propias solicitudes.
    if solicitud["id_estudiante"] != id_estudiante:
        raise PermissionError(
            "No tienes permiso para modificar esta solicitud."
        )

    # Solo una solicitud pendiente puede seguir siendo modificada.
    if solicitud["estado"] != "pendiente":
        raise ValueError(
            f"No se puede modificar una solicitud en estado "
            f"'{solicitud['estado']}'."
        )

    # Validación lógica de los datos socioeconómicos.
    if datos.dependientes_economicos > datos.integrantes_hogar:
        raise ValueError(
            "Los dependientes económicos no pueden superar "
            "el número de integrantes del hogar."
        )

    detalle = DetalleSolicitud(
        id_solicitud=id_solicitud,
        motivacion=datos.motivacion,
        situacion_economica=datos.situacion_economica,
        ingresos_familiares=datos.ingresos_familiares,
        integrantes_hogar=datos.integrantes_hogar,
        dependientes_economicos=datos.dependientes_economicos,
        ocupacion_responsable=datos.ocupacion_responsable,
        institucion_educativa=datos.institucion_educativa,
        carrera_area=datos.carrera_area,
        grado_semestre=datos.grado_semestre,
        promedio_academico=datos.promedio_academico,
        meta_academica=datos.meta_academica,
    )

    guardar_detalle_solicitud(detalle)

    return obtener_detalle_solicitud(id_solicitud)

# US-013 - Consultar solicitudes
def consultar_solicitudes_estudiante(id_estudiante: int) -> list[dict]:
    return obtener_solicitudes_por_estudiante(id_estudiante)


def consultar_solicitud(
    id_solicitud: int,
    id_estudiante: int
) -> dict:
    solicitud = obtener_solicitud_por_id(id_solicitud)

    if solicitud is None:
        raise ValueError("Solicitud no encontrada.")

    if solicitud["id_estudiante"] != id_estudiante:
        raise PermissionError(
            "No tienes permiso para consultar esta solicitud."
        )

    detalle = obtener_detalle_solicitud(id_solicitud)

    return {
        "solicitud": solicitud,
        "detalle": detalle
    }