from dataclasses import dataclass


@dataclass
class Evaluacion:
    id_solicitud: int
    id_evaluador: int
    id_asignador: int