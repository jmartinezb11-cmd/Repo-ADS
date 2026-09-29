from app.core.security import verify_password, crear_token

from app.repositories.estudiante_repository import (
    obtener_estudiante_por_email
)


MENSAJE_CREDENCIALES_INVALIDAS = "Correo o contraseña incorrectos."


def login_estudiante(email: str, password: str) -> dict:

    estudiante = obtener_estudiante_por_email(email)

    if estudiante is None:
        raise ValueError(MENSAJE_CREDENCIALES_INVALIDAS)

    if not verify_password(password, estudiante["password_hash"]):
        raise ValueError(MENSAJE_CREDENCIALES_INVALIDAS)

    if estudiante["estado_cuenta"] == "inactivo":
        raise ValueError(
            "Tu cuenta se encuentra inactiva. Contacta al administrador."
        )

    nombre_completo = (
        f"{estudiante['primer_nombre']} {estudiante['primer_apellido']}"
    )

    token = crear_token(
        id_estudiante=estudiante["id_estudiante"],
        rol=estudiante["rol"]
    )

    return {
        "token": token,
        "id_estudiante": estudiante["id_estudiante"],
        "nombre_completo": nombre_completo,
        "email": estudiante["email"],
        "rol": estudiante["rol"]
    }