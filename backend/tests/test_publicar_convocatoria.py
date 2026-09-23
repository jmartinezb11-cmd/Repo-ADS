from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_admin_puede_publicar_convocatoria_en_borrador():
    response = client.patch("/convocatorias/1/publicar?token=token-admin")
    assert response.status_code == 200
    assert response.json()["convocatoria"]["estado"] == "publicada"

def test_estudiante_no_puede_publicar():
    response = client.patch("/convocatorias/1/publicar?token=token-estudiante")
    assert response.status_code == 403

def test_convocatoria_inexistente_da_error():
    response = client.patch("/convocatorias/999/publicar?token=token-admin")
    assert response.status_code == 404

def test_no_se_puede_republicar_convocatoria_ya_publicada():
    response = client.patch("/convocatorias/2/publicar?token=token-admin")
    assert response.status_code == 400
    