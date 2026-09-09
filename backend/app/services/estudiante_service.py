from app.core.security import hash_password
from app.models.estudiante import Estudiante

from app.repositories.estudiante_repository import (
    crear_estudiante_completo,
    existe_estudiante_por_cui,
    existe_estudiante_por_email
)


def registrar_estudiante(
    estudiante: Estudiante,
    password: str,
    datos_academicos: dict,
    datos_socioeconomicos: dict,
    contacto_emergencia: dict
) -> int:

    if existe_estudiante_por_email(estudiante.email):
        raise ValueError(
            "El correo electrónico ya está registrado."
        )

    if existe_estudiante_por_cui(estudiante.cui):
        raise ValueError(
            "El CUI ya está registrado."
        )

    if not estudiante.discapacidad:
        estudiante.tipo_discapacidad = None

    estudiante.password_hash = hash_password(password)

    id_estudiante = crear_estudiante_completo(
        estudiante=estudiante,
        datos_academicos=datos_academicos,
        datos_socioeconomicos=datos_socioeconomicos,
        contacto_emergencia=contacto_emergencia
    )

    return id_estudiante