from fastapi.testclient import TestClient
from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role


def usuario_falso(rol: Role):
    def _override():
        return {"id": 1, "nombre": "Usuario de prueba", "rol": rol}
    return _override


client = TestClient(app)


def test_evaluador_puede_aprobar_documento_pendiente():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)
    response = client.patch(
        "/api/documentos/1/validar",
        json={"estado_validacion": "aprobado", "comentario_validacion": "Todo en orden."}
    )
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["documento"]["estado_validacion"] == "aprobado"


def test_estudiante_no_puede_validar():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)
    response = client.patch(
        "/api/documentos/1/validar",
        json={"estado_validacion": "aprobado"}
    )
    app.dependency_overrides.clear()
    assert response.status_code == 403


def test_documento_inexistente_da_error():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)
    response = client.patch(
        "/api/documentos/999/validar",
        json={"estado_validacion": "aprobado"}
    )
    app.dependency_overrides.clear()
    assert response.status_code == 400


def test_no_se_puede_revalidar_documento_ya_procesado():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)
    response = client.patch(
        "/api/documentos/2/validar",
        json={"estado_validacion": "rechazado"}
    )
    app.dependency_overrides.clear()
    assert response.status_code == 400


def test_estado_invalido_da_error():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)
    response = client.patch(
        "/api/documentos/1/validar",
        json={"estado_validacion": "no_valido"}
    )
    app.dependency_overrides.clear()
    assert response.status_code == 400
