import os
import uuid

from app.models.documento import Documento
from app.repositories.documento_repository import (
    crear_documento,
    listar_documentos_por_solicitud,
    obtener_documento_por_id,
)
from app.repositories.solicitud_repository import obtener_solicitud_por_id


CARPETA_DOCUMENTOS = "uploads/documentos"
EXTENSIONES_PERMITIDAS = [".pdf"]
TAMANIO_MAXIMO_BYTES = 5 * 1024 * 1024  # 5 MB


def cargar_documento(
    id_solicitud: int,
    id_estudiante: int,
    nombre_archivo: str,
    contenido: bytes
) -> dict:

    solicitud = obtener_solicitud_por_id(id_solicitud)

    if solicitud is None:
        raise ValueError("La solicitud no existe.")

    if solicitud["id_estudiante"] != id_estudiante:
        raise PermissionError(
            "No tienes permiso para subir documentos a esta solicitud."
        )

    extension = os.path.splitext(nombre_archivo)[1].lower()

    if extension not in EXTENSIONES_PERMITIDAS:
        raise ValueError("Solo se permiten archivos en formato PDF.")

    if len(contenido) > TAMANIO_MAXIMO_BYTES:
        raise ValueError("El archivo no puede superar los 5 MB.")

    if len(contenido) == 0:
        raise ValueError("El archivo está vacío.")

    os.makedirs(CARPETA_DOCUMENTOS, exist_ok=True)

    nombre_unico = f"{uuid.uuid4()}{extension}"
    ruta_archivo = os.path.join(CARPETA_DOCUMENTOS, nombre_unico)

    with open(ruta_archivo, "wb") as archivo_destino:
        archivo_destino.write(contenido)

    documento = Documento(
        id_solicitud=id_solicitud,
        nombre_archivo=nombre_archivo,
        tipo_archivo="pdf",
        ruta_archivo=ruta_archivo,
    )

    id_documento = crear_documento(documento)

    documento_guardado = obtener_documento_por_id(id_documento)

    return {
        "id_documento": documento_guardado["id_documento"],
        "id_solicitud": documento_guardado["id_solicitud"],
        "nombre_archivo": documento_guardado["nombre_archivo"],
        "tipo_archivo": documento_guardado["tipo_archivo"],
        "fecha_carga": documento_guardado["fecha_carga"],
    }


def obtener_documentos_de_solicitud(
    id_solicitud: int,
    id_estudiante: int
) -> list[dict]:

    solicitud = obtener_solicitud_por_id(id_solicitud)

    if solicitud is None:
        raise ValueError("La solicitud no existe.")

    if solicitud["id_estudiante"] != id_estudiante:
        raise PermissionError(
            "No tienes permiso para consultar los documentos de esta solicitud."
        )

    return listar_documentos_por_solicitud(id_solicitud)

# =========================================================
# US-016 - Validar documentación
# =========================================================
from app.repositories.documento_repository import (
    listar_documentos_para_revision,
    validar_documento,
)

ESTADOS_VALIDACION = ("aprobado", "rechazado")


class RecursoNoEncontrado(Exception):
    pass


def procesar_validacion(
    id_documento: int,
    estado_validacion: str,
    comentario_validacion: str | None,
    id_validador: int
) -> dict:

    if estado_validacion not in ESTADOS_VALIDACION:
        raise ValueError(
            "El estado de validación debe ser 'aprobado' o 'rechazado'."
        )

    comentario = (comentario_validacion or "").strip() or None

    if estado_validacion == "rechazado" and comentario is None:
        raise ValueError("Debes indicar el motivo del rechazo.")

    if obtener_documento_por_id(id_documento) is None:
        raise RecursoNoEncontrado("Documento no encontrado.")

    documento = validar_documento(
        id_documento,
        estado_validacion,
        comentario,
        id_validador
    )

    if documento is None:
        raise ValueError("Este documento ya fue validado o rechazado.")

    return documento


def listar_para_revision(id_solicitud: int) -> list[dict]:
    if obtener_solicitud_por_id(id_solicitud) is None:
        raise RecursoNoEncontrado("La solicitud no existe.")

    return listar_documentos_para_revision(id_solicitud)


def obtener_ruta_archivo(id_documento: int) -> tuple[str, str]:
    documento = obtener_documento_por_id(id_documento)

    if documento is None:
        raise RecursoNoEncontrado("Documento no encontrado.")

    if not os.path.exists(documento["ruta_archivo"]):
        raise RecursoNoEncontrado("El archivo no se encuentra en el servidor.")

    return documento["ruta_archivo"], documento["nombre_archivo"]
