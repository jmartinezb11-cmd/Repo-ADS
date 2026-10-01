from fastapi.testclient import TestClient
from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role


def usuario_falso(rol: Role):
    def _override():
        return {"id": 1, "nombre": "Usuario de prueba", "rol": rol}
    return _override


client = TestClient(app)


def test_acceso_permitido_estudiante():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)
    response = client.get("/roles-demo/estudiante")
    app.dependency_overrides.clear()
    assert response.status_code == 200


def test_acceso_rechazado_estudiante_en_ruta_admin():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)
    response = client.get("/roles-demo/admin")
    app.dependency_overrides.clear()
    assert response.status_code == 403


def test_acceso_permitido_admin():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)
    response = client.get("/roles-demo/admin")
    app.dependency_overrides.clear()
    assert response.status_code == 200
