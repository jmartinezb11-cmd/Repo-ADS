from fastapi.testclient import TestClient
from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role
import app.api.routes.solicitudes as solicitudes_route


def usuario_falso(rol: Role, id_usuario: int = 1):
    def _override():
        return {"id": id_usuario, "nombre": "Estudiante Demo", "rol": rol}
    return _override


client = TestClient(app)


def test_estudiante_puede_crear_solicitud(monkeypatch):
    def fake_registrar(id_estudiante, id_convocatoria):
        return {
            "id_solicitud": 1,
            "id_estudiante": id_estudiante,
            "id_convocatoria": id_convocatoria,
            "estado": "pendiente",
        }

    monkeypatch.setattr(solicitudes_route, "registrar_solicitud", fake_registrar)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)

    response = client.post("/api/solicitudes/convocatoria/1")

    app.dependency_overrides.clear()
    assert response.status_code == 201
    assert response.json()["solicitud"]["estado"] == "pendiente"


def test_admin_no_puede_crear_solicitud():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)
    response = client.post("/api/solicitudes/convocatoria/1")
    app.dependency_overrides.clear()
    assert response.status_code == 403


def test_convocatoria_no_publicada_da_error(monkeypatch):
    def fake_registrar(id_estudiante, id_convocatoria):
        raise ValueError("No se puede solicitar: la convocatoria está en estado 'borrador'.")

    monkeypatch.setattr(solicitudes_route, "registrar_solicitud", fake_registrar)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)

    response = client.post("/api/solicitudes/convocatoria/1")

    app.dependency_overrides.clear()
    assert response.status_code == 400


def test_solicitud_duplicada_da_error(monkeypatch):
    def fake_registrar(id_estudiante, id_convocatoria):
        raise ValueError("Ya existe una solicitud de este estudiante para esta convocatoria.")

    monkeypatch.setattr(solicitudes_route, "registrar_solicitud", fake_registrar)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)

    response = client.post("/api/solicitudes/convocatoria/1")

    app.dependency_overrides.clear()
    assert response.status_code == 400
