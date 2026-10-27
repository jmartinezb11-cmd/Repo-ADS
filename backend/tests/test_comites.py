
import pytest

from app.services import comite_service


def test_crear_comite_correctamente(monkeypatch):
    def crear_falso(nombre_comite, descripcion):
        return {
            "id_comite": 1,
            "nombre_comite": nombre_comite,
            "descripcion": descripcion,
            "estado": "ACTIVO"
        }

    monkeypatch.setattr(
        comite_service,
        "crear_comite_db",
        crear_falso
    )

    resultado = comite_service.crear_comite(
        "Comité Evaluador",
        "Evaluación de becas"
    )

    assert resultado["id_comite"] == 1
    assert resultado["estado"] == "ACTIVO"


def test_crear_comite_nombre_invalido():
    with pytest.raises(ValueError):
        comite_service.crear_comite("AB")


def test_asignar_miembro_correctamente(monkeypatch):
    monkeypatch.setattr(
        comite_service,
        "obtener_comite_db",
        lambda id_comite: {
            "id_comite": id_comite,
            "estado": "ACTIVO"
        }
    )

    monkeypatch.setattr(
        comite_service,
        "obtener_usuario_para_comite_db",
        lambda id_estudiante: {
            "id_estudiante": id_estudiante,
            "rol": "evaluador",
            "estado_cuenta": "activo"
        }
    )

    monkeypatch.setattr(
        comite_service,
        "asignar_miembro_db",
        lambda id_comite, id_estudiante, rol_comite: {
            "id_comite": id_comite,
            "id_estudiante": id_estudiante,
            "rol_comite": rol_comite
        }
    )

    resultado = comite_service.asignar_miembro_comite(
        1, 8, "EVALUADOR"
    )

    assert resultado["id_comite"] == 1
    assert resultado["id_estudiante"] == 8


def test_asignar_comite_inexistente(monkeypatch):
    monkeypatch.setattr(
        comite_service,
        "obtener_comite_db",
        lambda id_comite: None
    )

    with pytest.raises(LookupError):
        comite_service.asignar_miembro_comite(
            99999, 8, "EVALUADOR"
        )


def test_asignar_usuario_inexistente(monkeypatch):
    monkeypatch.setattr(
        comite_service,
        "obtener_comite_db",
        lambda id_comite: {"estado": "ACTIVO"}
    )

    monkeypatch.setattr(
        comite_service,
        "obtener_usuario_para_comite_db",
        lambda id_estudiante: None
    )

    with pytest.raises(LookupError):
        comite_service.asignar_miembro_comite(
            1, 99999, "EVALUADOR"
        )


def test_rechazar_estudiante_como_evaluador(monkeypatch):
    monkeypatch.setattr(
        comite_service,
        "obtener_comite_db",
        lambda id_comite: {"estado": "ACTIVO"}
    )

    monkeypatch.setattr(
        comite_service,
        "obtener_usuario_para_comite_db",
        lambda id_estudiante: {
            "rol": "estudiante",
            "estado_cuenta": "activo"
        }
    )

    with pytest.raises(ValueError):
        comite_service.asignar_miembro_comite(
            1, 1, "EVALUADOR"
        )


def test_rechazar_usuario_inactivo(monkeypatch):
    monkeypatch.setattr(
        comite_service,
        "obtener_comite_db",
        lambda id_comite: {"estado": "ACTIVO"}
    )

    monkeypatch.setattr(
        comite_service,
        "obtener_usuario_para_comite_db",
        lambda id_estudiante: {
            "rol": "evaluador",
            "estado_cuenta": "inactivo"
        }
    )

    with pytest.raises(ValueError):
        comite_service.asignar_miembro_comite(
            1, 8, "EVALUADOR"
        )


def test_consultar_comite_real(monkeypatch):
    monkeypatch.setattr(
        comite_service,
        "obtener_comite_db",
        lambda id_comite: {
            "id_comite": 1,
            "nombre_comite": "Comité Evaluador"
        }
    )

    monkeypatch.setattr(
        comite_service,
        "obtener_integrantes_comite_db",
        lambda id_comite: [{
            "id_integrante": 8,
            "nombre": "Usuario de prueba",
            "rol": "PRESIDENTE"
        }]
    )

    resultado = comite_service.consultar_comite_real(1)

    assert resultado["id_comite"] == 1
    assert len(resultado["integrantes"]) == 1
    assert resultado["integrantes"][0]["asignaciones"] == []
