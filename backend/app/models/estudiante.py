from dataclasses import dataclass
from datetime import date


@dataclass
class Estudiante:
    primer_nombre: str
    primer_apellido: str
    cui: str
    fecha_nacimiento: date
    genero: str
    nacionalidad: str
    telefono: str
    departamento: str
    municipio: str
    direccion_exacta: str
    email: str
    password_hash: str

    segundo_nombre: str | None = None
    segundo_apellido: str | None = None
    telefono_alternativo: str | None = None
    zona_aldea: str | None = None
    discapacidad: bool = False
    tipo_discapacidad: str | None = None
    pueblo_pertenencia: str | None = None