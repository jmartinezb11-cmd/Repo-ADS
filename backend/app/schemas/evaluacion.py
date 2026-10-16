from datetime import datetime

from pydantic import BaseModel, Field


class AsignarEvaluacionRequest(BaseModel):
    id_solicitud: int = Field(gt=0)
    id_evaluador: int = Field(gt=0)


class EvaluacionRespuesta(BaseModel):
    id_evaluacion: int
    id_solicitud: int
    id_evaluador: int
    id_asignador: int
    estado: str
    fecha_asignacion: datetime


class AsignacionEvaluador(BaseModel):
    id_evaluacion: int
    id_solicitud: int
    convocatoria: str
    estado: str
    fecha_asignacion: datetime


class SolicitudAsignable(BaseModel):
    id_solicitud: int
    estudiante: str
    convocatoria: str
    estado: str


class EvaluadorDisponible(BaseModel):
    id_evaluador: int
    nombre: str
    email: str