from datetime import datetime
from pydantic import BaseModel


class DocumentoRespuesta(BaseModel):
    id_documento: int
    id_solicitud: int
    nombre_archivo: str
    tipo_archivo: str
    fecha_carga: datetime