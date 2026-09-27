from app.models.convocatoria import Convocatoria
from app.repositories.convocatoria_repository import crear_convocatoria


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