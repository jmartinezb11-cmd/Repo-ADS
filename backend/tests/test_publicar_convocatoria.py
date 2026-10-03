from fastapi.testclient import TestClient
from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role
import app.api.routes.convocatorias as convocatorias_route


def usuario_falso(rol: Role):
    def _override():
        return {"id": 1, "nombre": "Usuario de prueba", "rol": rol}
    return _override


client = TestClient(app)


def test_admin_puede_publicar_convocatoria_en_borrador(monkeypatch):
    def fake_cambiar_estado(id_convocatoria):
        return {"id_convocatoria": id_convocatoria, "estado": "publicada"}

    monkeypatch.setattr(
        convocatorias_route, "cambiar_estado_a_publicada", fake_cambiar_estado
    )
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.patch("/api/convocatorias/1/publicar")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["convocatoria"]["estado"] == "publicada"


def test_estudiante_no_puede_publicar():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)
    response = client.patch("/api/convocatorias/1/publicar")
    app.dependency_overrides.clear()
    assert response.status_code == 403


def test_convocatoria_inexistente_da_error(monkeypatch):
    def fake_cambiar_estado(id_convocatoria):
        raise ValueError("Convocatoria no encontrada.")

    monkeypatch.setattr(
        convocatorias_route, "cambiar_estado_a_publicada", fake_cambiar_estado
    )
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.patch("/api/convocatorias/999/publicar")

    app.dependency_overrides.clear()
    assert response.status_code == 400


def test_no_se_puede_republicar_convocatoria_ya_publicada(monkeypatch):
    def fake_cambiar_estado(id_convocatoria):
        raise ValueError("No se puede publicar una convocatoria en estado 'publicada'.")

    monkeypatch.setattr(
        convocatorias_route, "cambiar_estado_a_publicada", fake_cambiar_estado
    )
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.patch("/api/convocatorias/2/publicar")

    app.dependency_overrides.clear()
    assert response.status_code == 400
