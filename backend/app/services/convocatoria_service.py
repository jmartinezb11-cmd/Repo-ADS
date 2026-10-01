from app.models.convocatoria import Convocatoria
from app.repositories.convocatoria_repository import (
    crear_convocatoria,
    obtener_convocatoria_por_id,
    listar_convocatorias,
    actualizar_estado_convocatoria
)


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

ESTADOS_VALIDOS_PARA_CERRAR = ["publicada"]


def cerrar_convocatoria(id_convocatoria: int) -> dict:

    convocatoria = obtener_convocatoria_por_id(id_convocatoria)

    if convocatoria is None:
        raise ValueError("La convocatoria no existe.")

    if convocatoria["estado"] not in ESTADOS_VALIDOS_PARA_CERRAR:
        raise ValueError(
            "No se puede cerrar una convocatoria en estado "
            f"'{convocatoria['estado']}'. Solo se pueden cerrar "
            "convocatorias que estén 'publicada'."
        )

    actualizado = actualizar_estado_convocatoria(id_convocatoria, "cerrada")

    if not actualizado:
        raise ValueError("No fue posible cerrar la convocatoria.")

    return {
        "id_convocatoria": id_convocatoria,
        "titulo": convocatoria["titulo"],
        "estado": "cerrada"
    }


def obtener_todas_las_convocatorias() -> list[dict]:
    return listar_convocatorias()