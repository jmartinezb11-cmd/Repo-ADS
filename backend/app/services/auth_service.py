from app.core.security import verify_password

from app.repositories.estudiante_repository import (
    obtener_estudiante_por_email
)


# Mensaje genérico a propósito: nunca se debe indicar si falló
# el email o la contraseña, para no darle pistas a un atacante
# sobre qué correos existen registrados (US-029).
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

    return {
        "id_estudiante": estudiante["id_estudiante"],
        "nombre_completo": nombre_completo,
        "email": estudiante["email"],
        # Por ahora todo registro es de rol "estudiante", ya que el
        # sistema todavía no tiene un mecanismo de roles en la base
        # de datos (pendiente de definir en US-028 con Pablo).
        "rol": "estudiante"
    }