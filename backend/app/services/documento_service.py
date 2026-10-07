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