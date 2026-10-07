from dataclasses import dataclass


@dataclass
class Documento:
    id_solicitud: int
    nombre_archivo: str
    tipo_archivo: str
    ruta_archivo: str