from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DetalleSolicitud:
    id_solicitud: int
    motivacion: str
    situacion_economica: str
    ingresos_familiares: Decimal
    integrantes_hogar: int
    dependientes_economicos: int
    ocupacion_responsable: str
    institucion_educativa: str
    carrera_area: str
    grado_semestre: str
    promedio_academico: Decimal
    meta_academica: str