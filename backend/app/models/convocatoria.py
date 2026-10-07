from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Convocatoria:
    titulo: str
    descripcion: str
    tipo_beca: str
    institucion: str
    fecha_apertura: date
    fecha_cierre: date
    nivel_educativo: str
    requisitos: str

    monto_beneficio: Decimal | None = None
    cupos_disponibles: int | None = None
    estado: str = "borrador"