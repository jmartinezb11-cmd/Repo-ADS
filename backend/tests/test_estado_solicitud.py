
import pytest

from app.services import solicitud_service


def test_consultar_estado_correctamente(monkeypatch):
    monkeypatch.setattr(
        solicitud_service,
        "obtener_solicitud_por_id",
        lambda id_solicitud: {
            "id_solicitud": 1,
            "id_estudiante": 5,
            "id_convocatoria": 3,
            "estado": "pendiente",
            "fecha_ultima_actualizacion": None
        }
    )

    resultado = solicitud_service.consultar_estado_solicitud(
        id_solicitud=1,
        id_estudiante=5
    )

    assert resultado["id_solicitud"] == 1
    assert resultado["estado"] == "pendiente"


def test_consultar_solicitud_inexistente(monkeypatch):
    monkeypatch.setattr(
        solicitud_service,
        "obtener_solicitud_por_id",
        lambda id_solicitud: None
    )

    with pytest.raises(ValueError):
        solicitud_service.consultar_estado_solicitud(
            id_solicitud=99999,
            id_estudiante=5
        )


def test_impedir_consulta_de_otro_estudiante(monkeypatch):
    monkeypatch.setattr(
        solicitud_service,
        "obtener_solicitud_por_id",
        lambda id_solicitud: {
            "id_solicitud": 1,
            "id_estudiante": 5
        }
    )

    with pytest.raises(PermissionError):
        solicitud_service.consultar_estado_solicitud(
            id_solicitud=1,
            id_estudiante=9
        )
