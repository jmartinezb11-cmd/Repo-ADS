from dataclasses import dataclass


@dataclass
class ResultadoValidacion:
    estado_validacion: str  # "aprobado" o "rechazado"
    comentario_validacion: str | None = None
