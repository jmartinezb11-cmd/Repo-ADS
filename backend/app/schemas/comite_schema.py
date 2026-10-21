from pydantic import BaseModel
from typing import List, Optional

class IntegranteComite(BaseModel):
    id_integrante: int
    nombre: str
    rol: str # Ej: Presidente, Evaluador, Secretario
    asignaciones: List[str] # Ej: ["Evaluacion Convocatoria A1", "Revision Final"]

class ComiteResponse(BaseModel):
    id_comite: int
    nombre_comite: str
    integrantes: List[IntegranteComite]


from datetime import datetime
from pydantic import Field


class CrearComiteRequest(BaseModel):
    nombre_comite: str = Field(min_length=3, max_length=150)
    descripcion: Optional[str] = None


class CrearComiteResponse(BaseModel):
    id_comite: int
    nombre_comite: str
    descripcion: Optional[str] = None
    estado: str
    fecha_creacion: datetime


class AsignarMiembroRequest(BaseModel):
    id_estudiante: int = Field(gt=0)
    rol_comite: str = Field(
        pattern="^(PRESIDENTE|EVALUADOR|SECRETARIO)$"
    )


class AsignarMiembroResponse(BaseModel):
    id_miembro: int
    id_comite: int
    id_estudiante: int
    rol_comite: str
    fecha_asignacion: datetime
