# Servicio con MOCK para US-023: Consultar comité

MOCK_COMITE = {
    "id_comite": 101,
    "nombre_comite": "Comité Evaluador de Proyectos 2026",
    "integrantes": [
        {
            "id_integrante": 1,
            "nombre": "Dr. Carlos Mendoza",
            "rol": "Presidente",
            "asignaciones": ["Evaluación Convocatoria A1", "Revisión Final"]
        },
        {
            "id_integrante": 2,
            "nombre": "Ing. Ana Lucía Morales",
            "rol": "Evaluador Senior",
            "asignaciones": ["Evaluación Propuestas US-021"]
        },
        {
            "id_integrante": 3,
            "nombre": "Lic. Luis González",
            "rol": "Secretario",
            "asignaciones": ["Control de actas y seguimiento"]
        }
    ]
}

def obtener_integrantes_comite_mock(id_comite: int):
    # Cuando desbloqueen la US-21 o la base de datos, aquí se hará la consulta real
    return MOCK_COMITE


from app.repositories.comite_repository import crear_comite_db


def crear_comite(nombre_comite: str, descripcion: str | None = None):
    nombre_comite = nombre_comite.strip()

    if len(nombre_comite) < 3:
        raise ValueError(
            "El nombre del comité debe tener al menos 3 caracteres."
        )

    if descripcion is not None:
        descripcion = descripcion.strip() or None

    return crear_comite_db(nombre_comite, descripcion)


from app.repositories.comite_repository import (
    obtener_comite_db,
    obtener_usuario_para_comite_db,
    asignar_miembro_db
)


def asignar_miembro_comite(
    id_comite: int,
    id_estudiante: int,
    rol_comite: str
):
    comite = obtener_comite_db(id_comite)

    if comite is None:
        raise LookupError("El comité no existe.")

    if comite["estado"] != "ACTIVO":
        raise ValueError("El comité no está activo.")

    usuario = obtener_usuario_para_comite_db(id_estudiante)

    if usuario is None:
        raise LookupError("El usuario no existe.")

    if usuario["rol"] not in ("evaluador", "administrador"):
        raise ValueError(
            "Solo los evaluadores y administradores "
            "pueden ser miembros del comité."
        )

    if usuario["estado_cuenta"] == "inactivo":
        raise ValueError(
            "No se pueden asignar usuarios inactivos."
        )

    return asignar_miembro_db(
        id_comite=id_comite,
        id_estudiante=id_estudiante,
        rol_comite=rol_comite
    )


from app.repositories.comite_repository import obtener_integrantes_comite_db


def consultar_comite_real(id_comite: int):
    comite = obtener_comite_db(id_comite)

    if comite is None:
        raise LookupError("El comité no existe.")

    integrantes = obtener_integrantes_comite_db(id_comite)

    for integrante in integrantes:
        integrante["asignaciones"] = []

    return {
        "id_comite": comite["id_comite"],
        "nombre_comite": comite["nombre_comite"],
        "integrantes": integrantes
    }
