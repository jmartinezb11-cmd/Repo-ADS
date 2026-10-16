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
    