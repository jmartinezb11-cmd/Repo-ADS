# --- MOCK temporal, mientras US-014 crea la tabla real "documentos" ---
# Cuando esté lista, estas funciones se reemplazan por consultas psycopg2
# reales, siguiendo el mismo patrón de convocatoria_repository.py

from app.core.documentos_mock import DOCUMENTOS_DB


def obtener_documento_por_id(id_documento: int) -> dict | None:
    return DOCUMENTOS_DB.get(id_documento)


def validar_documento(
    id_documento: int,
    estado_validacion: str,
    comentario_validacion: str | None
) -> dict | None:

    documento = DOCUMENTOS_DB.get(id_documento)

    if documento is None:
        return None

    documento["estado_validacion"] = estado_validacion
    documento["comentario_validacion"] = comentario_validacion

    return documento
