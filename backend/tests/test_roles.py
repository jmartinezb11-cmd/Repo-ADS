from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_acceso_permitido_estudiante():
    response = client.get("/roles-demo/estudiante?token=token-estudiante")
    assert response.status_code == 200

def test_acceso_rechazado_estudiante_en_ruta_admin():
    response = client.get("/roles-demo/admin?token=token-estudiante")
    assert response.status_code == 403

def test_usuario_no_autenticado():
    response = client.get("/roles-demo/estudiante?token=token-inexistente")
    assert response.status_code == 401
    