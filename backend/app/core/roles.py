from enum import Enum

class Role(str, Enum):
    ESTUDIANTE = "estudiante"
    EVALUADOR = "evaluador"
    ADMINISTRADOR = "administrador"
