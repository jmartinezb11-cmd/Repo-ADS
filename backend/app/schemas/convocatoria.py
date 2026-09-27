from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class ConvocatoriaCrear(BaseModel):
    titulo: str = Field(min_length=3, max_length=150)
    descripcion: str = Field(min_length=10)
    tipo_beca: str = Field(min_length=2, max_length=100)
    institucion: str = Field(min_length=2, max_length=150)

    fecha_apertura: date
    fecha_cierre: date

    nivel_educativo: str = Field(min_length=2, max_length=50)
    requisitos: str = Field(min_length=5)

    monto_beneficio: Decimal | None = Field(default=None, ge=0)
    cupos_disponibles: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_cierre <= self.fecha_apertura:
            raise ValueError(
                "La fecha de cierre debe ser posterior a la fecha de apertura."
            )

        return self