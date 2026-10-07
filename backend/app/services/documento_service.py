from app.repositories.documento_repository import (
    obtener_documento_por_id,
    validar_documento,
)

ESTADOS_VALIDOS = ("aprobado", "rechazado")


def procesar_validacion(
    id_documento: int,
    estado_validacion: str,
    comentario_validacion: str | None
) -> dict:

    if estado_validacion not in ESTADOS_VALIDOS:
        raise ValueError(
            f"Estado de validación inválido. Debe ser uno de: {ESTADOS_VALIDOS}."
        )

    documento = obtener_documento_por_id(id_documento)

    if documento is None:
        raise ValueError("Documento no encontrado.")

    if documento["estado_validacion"] != "pendiente":
        raise ValueError(
            f"Este documento ya fue procesado "
            f"(estado actual: '{documento['estado_validacion']}')."
        )

    resultado = validar_documento(
        id_documento,
        estado_validacion,
        comentario_validacion
    )

    return resultado
