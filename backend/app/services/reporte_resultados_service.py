
from datetime import datetime

from app.repositories.convocatoria_repository import (
    obtener_convocatoria_por_id
)
from app.repositories.reporte_resultados_repository import (
    listar_resultados
)


ESTADOS_VALIDOS = {"aprobada", "rechazada"}


def generar_reporte_resultados(
    id_convocatoria: int | None = None,
    estado: str | None = None
) -> dict:

    estado = (estado or "").strip().lower() or None

    if estado is not None and estado not in ESTADOS_VALIDOS:
        raise ValueError(
            "El estado debe ser 'aprobada' o 'rechazada'."
        )

    if id_convocatoria is not None:
        if obtener_convocatoria_por_id(id_convocatoria) is None:
            raise LookupError("Convocatoria no encontrada.")

    resultados = listar_resultados(id_convocatoria, estado)

    aprobadas = sum(
        1 for fila in resultados
        if fila["resultado"] == "aprobada"
    )

    rechazadas = sum(
        1 for fila in resultados
        if fila["resultado"] == "rechazada"
    )

    total = len(resultados)

    return {
        "filtros": {
            "id_convocatoria": id_convocatoria,
            "estado": estado
        },
        "generado_en": datetime.now().isoformat(
            timespec="seconds"
        ),
        "resumen": {
            "total_resueltas": total,
            "aprobadas": aprobadas,
            "rechazadas": rechazadas,
            "porcentaje_aprobacion": (
                round(aprobadas * 100 / total, 2)
                if total else 0
            )
        },
        "resultados": resultados
    }
