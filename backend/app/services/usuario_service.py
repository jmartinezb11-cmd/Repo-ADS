from app.repositories.estudiante_repository import (
    listar_estudiantes,
    obtener_estudiante_por_id,
    actualizar_estado_cuenta
)


def _a_resumen(estudiante: dict) -> dict:
    return {
        "id_estudiante": estudiante["id_estudiante"],
        "nombre_completo": (
            f"{estudiante['primer_nombre']} {estudiante['primer_apellido']}"
        ),
        "email": estudiante["email"],
        "rol": estudiante["rol"],
        "estado_cuenta": estudiante["estado_cuenta"]
    }


def obtener_lista_usuarios() -> list[dict]:
    estudiantes = listar_estudiantes()

    return [_a_resumen(estudiante) for estudiante in estudiantes]


def obtener_usuario(id_estudiante: int) -> dict:
    estudiante = obtener_estudiante_por_id(id_estudiante)

    if estudiante is None:
        raise ValueError("Usuario no encontrado.")

    return _a_resumen(estudiante)


def cambiar_estado_usuario(
    id_estudiante: int,
    nuevo_estado: str,
    usuario_actual: dict
) -> dict:

    estudiante = obtener_estudiante_por_id(id_estudiante)

    if estudiante is None:
        raise ValueError("Usuario no encontrado.")

    if (
        usuario_actual["id"] == id_estudiante
        and nuevo_estado == "inactivo"
    ):
        raise ValueError(
            "No puedes desactivar tu propia cuenta de administrador."
        )

    actualizado = actualizar_estado_cuenta(id_estudiante, nuevo_estado)

    if not actualizado:
        raise ValueError("No fue posible actualizar el estado.")

    return {
        "id_estudiante": id_estudiante,
        "nuevo_estado": nuevo_estado
    }