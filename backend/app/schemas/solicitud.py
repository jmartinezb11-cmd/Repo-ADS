from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class SolicitudRespuesta(BaseModel):
    id_solicitud: int
    id_estudiante: int
    id_convocatoria: int
    estado: str
    fecha_creacion: datetime


# US-011 - Completar solicitud

class CompletarSolicitudRequest(BaseModel):
    motivacion: str = Field(min_length=10, max_length=2000)
    situacion_economica: str = Field(min_length=10, max_length=2000)

    ingresos_familiares: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

    integrantes_hogar: int = Field(gt=0)
    dependientes_economicos: int = Field(ge=0)

    ocupacion_responsable: str = Field(min_length=2, max_length=150)
    institucion_educativa: str = Field(min_length=2, max_length=200)
    carrera_area: str = Field(min_length=2, max_length=200)
    grado_semestre: str = Field(min_length=1, max_length=100)

    promedio_academico: Decimal = Field(
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2
    )

    meta_academica: str = Field(min_length=10, max_length=2000)

    @field_validator(
        "motivacion",
        "situacion_economica",
        "ocupacion_responsable",
        "institucion_educativa",
        "carrera_area",
        "grado_semestre",
        "meta_academica"
    )
    @classmethod
    def validar_texto_no_vacio(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("El campo no puede estar vacío.")

        return valor


class DetalleSolicitudRespuesta(CompletarSolicitudRequest):
    id_detalle: int
    id_solicitud: int
    fecha_actualizacion: datetime