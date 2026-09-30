from app.models.convocatoria import Convocatoria
from app.repositories.convocatoria_repository import (
    crear_convocatoria,
    obtener_convocatorias,
    obtener_convocatoria_por_id,
    actualizar_convocatoria,
    publicar_convocatoria,
)



# US-005 - Crear convocatoria

def registrar_convocatoria(convocatoria: Convocatoria) -> int:
    if convocatoria.fecha_cierre <= convocatoria.fecha_apertura:
        raise ValueError(
            "La fecha de cierre debe ser posterior a la fecha de apertura."
        )

    if (
        convocatoria.monto_beneficio is not None
        and convocatoria.monto_beneficio < 0
    ):
        raise ValueError(
            "El monto del beneficio no puede ser negativo."
        )

    if (
        convocatoria.cupos_disponibles is not None
        and convocatoria.cupos_disponibles < 0
    ):
        raise ValueError(
            "Los cupos disponibles no pueden ser negativos."
        )

    convocatoria.estado = "borrador"

    return crear_convocatoria(convocatoria)



# US-008 - Consultar convocatorias

def listar_convocatorias() -> list:
    return obtener_convocatorias()


def buscar_convocatoria(id_convocatoria: int) -> dict:
    convocatoria = obtener_convocatoria_por_id(id_convocatoria)

    if convocatoria is None:
        raise ValueError("Convocatoria no encontrada.")

    return convocatoria



# US-006 - Editar convocatoria

def editar_convocatoria(
    id_convocatoria: int,
    datos: dict
) -> dict:

    convocatoria = obtener_convocatoria_por_id(id_convocatoria)

    if convocatoria is None:
        raise ValueError("Convocatoria no encontrada.")

    if convocatoria["estado"] != "borrador":
        raise ValueError(
            "Solo se pueden editar convocatorias en estado borrador."
        )

    actualizado = actualizar_convocatoria(
        id_convocatoria,
        datos
    )

    if not actualizado:
        raise ValueError(
            "No se pudo actualizar la convocatoria."
        )

    return obtener_convocatoria_por_id(id_convocatoria)



# US-007 - Publicar convocatoria

def cambiar_estado_a_publicada(
    id_convocatoria: int
) -> dict:

    convocatoria = obtener_convocatoria_por_id(id_convocatoria)

    if convocatoria is None:
        raise ValueError("Convocatoria no encontrada.")

    if convocatoria["estado"] != "borrador":
        raise ValueError(
            f"No se puede publicar una convocatoria "
            f"en estado '{convocatoria['estado']}'."
        )

    publicada = publicar_convocatoria(id_convocatoria)

    if publicada is None:
        raise ValueError(
            "No se pudo publicar la convocatoria."
        )

    return publicada