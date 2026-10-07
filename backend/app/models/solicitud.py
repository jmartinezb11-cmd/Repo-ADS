from dataclasses import dataclass


@dataclass
class Solicitud:
    id_estudiante: int
    id_convocatoria: int
    estado: str = "pendiente"
