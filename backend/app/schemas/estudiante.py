from datetime import date

from pydantic import BaseModel, EmailStr, Field, model_validator


class DatosAcademicosRegistro(BaseModel):
    nivel_educativo: str

    establecimiento_educativo: str | None = None
    grado_actual: str | None = None
    jornada: str | None = None
    sector: str | None = None
    promedio_notas: float | None = None
    especialidad: str | None = None

    universidad: str | None = None
    facultad_escuela: str | None = None
    carrera: str | None = None
    anio_semestre_actual: str | None = None
    carnet_universitario: str | None = None
    cum: float | None = None
    creditos_aprobados: int | None = None
    modalidad: str | None = None

    @model_validator(mode="after")
    def validar_nivel_educativo(self):

        nivel = self.nivel_educativo.strip().lower()

        niveles_permitidos = [
            "basico",
            "básico",
            "bachillerato",
            "perito",
            "universitario"
        ]

        if nivel not in niveles_permitidos:
            raise ValueError(
                "El nivel educativo debe ser básico, bachillerato, "
                "perito o universitario."
            )

        if nivel == "universitario":
            if not self.universidad:
                raise ValueError(
                    "La universidad es obligatoria para nivel universitario."
                )

            if not self.carrera:
                raise ValueError(
                    "La carrera es obligatoria para nivel universitario."
                )

            if not self.anio_semestre_actual:
                raise ValueError(
                    "El año o semestre actual es obligatorio "
                    "para nivel universitario."
                )

        else:
            if not self.establecimiento_educativo:
                raise ValueError(
                    "El establecimiento educativo es obligatorio."
                )

            if not self.grado_actual:
                raise ValueError(
                    "El grado actual es obligatorio."
                )

            if not self.jornada:
                raise ValueError(
                    "La jornada es obligatoria."
                )

        if self.promedio_notas is not None:
            if self.promedio_notas < 0 or self.promedio_notas > 100:
                raise ValueError(
                    "El promedio de notas debe estar entre 0 y 100."
                )

        if self.cum is not None:
            if self.cum < 0 or self.cum > 100:
                raise ValueError(
                    "El CUM debe estar entre 0 y 100."
                )

        if self.creditos_aprobados is not None:
            if self.creditos_aprobados < 0:
                raise ValueError(
                    "Los créditos aprobados no pueden ser negativos."
                )

        return self


class DatosSocioeconomicosRegistro(BaseModel):
    ingreso_familiar_mensual: float | None = None
    numero_miembros_nucleo: int | None = None
    ocupacion_padre: str | None = None
    ocupacion_madre: str | None = None
    ocupacion_encargado: str | None = None
    tipo_vivienda: str | None = None
    dependientes_economicos: int | None = None

    @model_validator(mode="after")
    def validar_datos_socioeconomicos(self):

        if (
            self.ingreso_familiar_mensual is not None
            and self.ingreso_familiar_mensual < 0
        ):
            raise ValueError(
                "El ingreso familiar mensual no puede ser negativo."
            )

        if (
            self.numero_miembros_nucleo is not None
            and self.numero_miembros_nucleo <= 0
        ):
            raise ValueError(
                "El número de miembros del núcleo familiar debe ser mayor a 0."
            )

        if (
            self.dependientes_economicos is not None
            and self.dependientes_economicos < 0
        ):
            raise ValueError(
                "Los dependientes económicos no pueden ser negativos."
            )

        return self


class ContactoEmergenciaRegistro(BaseModel):
    nombre_encargado: str = Field(
        min_length=2,
        max_length=150
    )

    parentesco: str = Field(
        min_length=2,
        max_length=50
    )

    telefono_emergencia: str = Field(
        min_length=8,
        max_length=20
    )


class EstudianteRegistro(BaseModel):
    primer_nombre: str = Field(
        min_length=2,
        max_length=50
    )

    segundo_nombre: str | None = Field(
        default=None,
        max_length=50
    )

    primer_apellido: str = Field(
        min_length=2,
        max_length=50
    )

    segundo_apellido: str | None = Field(
        default=None,
        max_length=50
    )

    cui: str = Field(
        min_length=13,
        max_length=13
    )

    fecha_nacimiento: date

    genero: str = Field(
        min_length=1,
        max_length=20
    )

    nacionalidad: str = Field(
        min_length=2,
        max_length=50
    )

    telefono: str = Field(
        min_length=8,
        max_length=20
    )

    telefono_alternativo: str | None = Field(
        default=None,
        max_length=20
    )

    departamento: str = Field(
        min_length=2,
        max_length=100
    )

    municipio: str = Field(
        min_length=2,
        max_length=100
    )

    zona_aldea: str | None = Field(
        default=None,
        max_length=100
    )

    direccion_exacta: str = Field(
        min_length=5,
        max_length=255
    )

    discapacidad: bool = False

    tipo_discapacidad: str | None = Field(
        default=None,
        max_length=100
    )

    pueblo_pertenencia: str | None = Field(
        default=None,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )

    datos_academicos: DatosAcademicosRegistro
    datos_socioeconomicos: DatosSocioeconomicosRegistro
    contacto_emergencia: ContactoEmergenciaRegistro

    @model_validator(mode="after")
    def validar_estudiante(self):

        # CUI solo numérico
        if not self.cui.isdigit():
            raise ValueError(
                "El CUI debe contener únicamente números."
            )

        # Contraseña
        if not any(c.isupper() for c in self.password):
            raise ValueError(
                "La contraseña debe contener al menos una letra mayúscula."
            )

        if not any(c.isdigit() for c in self.password):
            raise ValueError(
                "La contraseña debe contener al menos un número."
            )

        if not any(
            not c.isalnum()
            for c in self.password
        ):
            raise ValueError(
                "La contraseña debe contener al menos un carácter especial."
            )

        # Discapacidad
        if self.discapacidad and not self.tipo_discapacidad:
            raise ValueError(
                "Debe indicar el tipo de discapacidad."
            )

        return self