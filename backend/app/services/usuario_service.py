from app.repositories.estudiante_repository import (
    listar_estudiantes,
    obtener_estudiante_por_id,
    actualizar_estado_cuenta,
    actualizar_rol_estudiante
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


def cambiar_rol_usuario(
    id_estudiante: int,
    nuevo_rol: str,
    usuario_actual: dict
) -> dict:

    if usuario_actual["rol"] != "administrador":
        raise PermissionError(
            "No tienes permisos para cambiar roles."
        )

    if usuario_actual["id"] == id_estudiante:
        raise ValueError(
            "No puedes modificar tu propio rol."
        )

    estudiante = obtener_estudiante_por_id(id_estudiante)

    if estudiante is None:
        raise LookupError("Usuario no encontrado.")

    if estudiante["rol"] == "administrador":
        raise ValueError(
            "No se permite modificar el rol de un administrador."
        )

    if nuevo_rol not in ("estudiante", "evaluador"):
        raise ValueError("Rol no permitido.")

    if estudiante["rol"] == nuevo_rol:
        raise ValueError(
            "El usuario ya tiene asignado ese rol."
        )

    actualizado = actualizar_rol_estudiante(
        id_estudiante,
        nuevo_rol
    )

    if not actualizado:
        raise ValueError(
            "No fue posible actualizar el rol."
        )

    return {
        "id_estudiante": id_estudiante,
        "nuevo_rol": nuevo_rol
    }
