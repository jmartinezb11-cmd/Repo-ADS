from datetime import datetime
from pydantic import BaseModel


class SolicitudRespuesta(BaseModel):
    id_solicitud: int
    id_estudiante: int
    id_convocatoria: int
    estado: str
    fecha_creacion: datetime
