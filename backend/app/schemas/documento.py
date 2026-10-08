from datetime import datetime
from pydantic import BaseModel


class DocumentoRespuesta(BaseModel):
    id_documento: int
    id_solicitud: int
    nombre_archivo: str
    tipo_archivo: str
    fecha_carga: datetime

# US-016 - Validar documentación
from typing import Literal


class ValidarDocumento(BaseModel):
    estado_validacion: Literal["aprobado", "rechazado"]
    comentario_validacion: str | None = None


class DocumentoRevisionRespuesta(BaseModel):
    id_documento: int
    id_solicitud: int
    nombre_archivo: str
    tipo_archivo: str
    fecha_carga: datetime
    estado_validacion: str
    comentario_validacion: str | None = None
    fecha_validacion: datetime | None = None
