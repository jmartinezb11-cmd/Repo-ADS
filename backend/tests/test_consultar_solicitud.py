from fastapi.testclient import TestClient

from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role
import app.api.routes.solicitudes as solicitudes_route


client = TestClient(app)


def usuario_estudiante(id_usuario: int = 1):
    def _override():
        return {
            "id": id_usuario,
            "nombre": "Estudiante Demo",
            "rol": Role.ESTUDIANTE
        }

    return _override


# US-013 - Consultar solicitudes


def test_estudiante_puede_listar_sus_solicitudes(monkeypatch):
    solicitudes_mock = [
        {
            "id_solicitud": 1,
            "id_estudiante": 1,
            "id_convocatoria": 1,
            "convocatoria": "Beca Universitaria",
            "estado": "pendiente",
            "fecha_creacion": "2026-10-08T10:00:00",
            "fecha_ultima_actualizacion": "2026-10-08T10:30:00"
        }
    ]

    def fake_consultar(id_estudiante):
        return solicitudes_mock

    monkeypatch.setattr(
        solicitudes_route,
        "consultar_solicitudes_estudiante",
        fake_consultar
    )

    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    response = client.get(
        "/api/solicitudes/mis-solicitudes"
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert len(response.json()["solicitudes"]) == 1
    assert response.json()["solicitudes"][0]["id_estudiante"] == 1
    assert response.json()["solicitudes"][0]["estado"] == "pendiente"


def test_estudiante_puede_consultar_solicitud_propia(monkeypatch):
    resultado_mock = {
        "solicitud": {
            "id_solicitud": 1,
            "id_estudiante": 1,
            "id_convocatoria": 1,
            "estado": "pendiente"
        },
        "detalle": {
            "id_detalle": 1,
            "id_solicitud": 1,
            "motivacion": "Deseo continuar mis estudios."
        }
    }

    def fake_consultar(id_solicitud, id_estudiante):
        return resultado_mock

    monkeypatch.setattr(
        solicitudes_route,
        "consultar_solicitud",
        fake_consultar
    )

    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    response = client.get(
        "/api/solicitudes/1"
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["solicitud"]["id_solicitud"] == 1
    assert response.json()["solicitud"]["id_estudiante"] == 1
    assert response.json()["detalle"]["id_solicitud"] == 1


def test_solicitud_inexistente_da_404(monkeypatch):
    def fake_consultar(id_solicitud, id_estudiante):
        raise ValueError("Solicitud no encontrada.")

    monkeypatch.setattr(
        solicitudes_route,
        "consultar_solicitud",
        fake_consultar
    )

    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    response = client.get(
        "/api/solicitudes/999999"
    )

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitud no encontrada."


def test_estudiante_no_puede_consultar_solicitud_ajena(monkeypatch):
    def fake_consultar(id_solicitud, id_estudiante):
        raise PermissionError(
            "No tienes permiso para consultar esta solicitud."
        )

    monkeypatch.setattr(
        solicitudes_route,
        "consultar_solicitud",
        fake_consultar
    )

    app.dependency_overrides[get_current_user] = usuario_estudiante(2)

    response = client.get(
        "/api/solicitudes/1"
    )

    app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "No tienes permiso para consultar esta solicitud."
    )


def test_solicitud_sin_detalle_puede_consultarse(monkeypatch):
    resultado_mock = {
        "solicitud": {
            "id_solicitud": 2,
            "id_estudiante": 1,
            "id_convocatoria": 2,
            "estado": "pendiente"
        },
        "detalle": None
    }

    def fake_consultar(id_solicitud, id_estudiante):
        return resultado_mock

    monkeypatch.setattr(
        solicitudes_route,
        "consultar_solicitud",
        fake_consultar
    )

    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    response = client.get(
        "/api/solicitudes/2"
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["solicitud"]["id_solicitud"] == 2
    assert response.json()["detalle"] is None