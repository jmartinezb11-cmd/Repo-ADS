import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role
import app.services.documento_service as documento_service


PDF = b"%PDF-1.4 prueba"

client = TestClient(app)


def usuario_falso(id_usuario: int = 5):
    def _override():
        return {
            "id": id_usuario,
            "nombre": "Estudiante de prueba",
            "rol": Role.ESTUDIANTE,
        }
    return _override


def solicitud_en_estado(estado: str, id_estudiante: int = 5):
    return lambda id_solicitud: {
        "id_solicitud": id_solicitud,
        "id_estudiante": id_estudiante,
        "estado": estado,
    }


@pytest.fixture(autouse=True)
def limpiar_overrides():
    yield
    app.dependency_overrides.clear()


# ---------- Service ----------

@pytest.mark.parametrize("estado", ["enviada", "aprobada", "rechazada"])
def test_no_se_cargan_documentos_despues_del_envio(monkeypatch, tmp_path, estado):
    guardados = []

    monkeypatch.setattr(documento_service, "CARPETA_DOCUMENTOS", str(tmp_path))
    monkeypatch.setattr(
        documento_service, "obtener_solicitud_por_id", solicitud_en_estado(estado)
    )
    monkeypatch.setattr(
        documento_service, "crear_documento",
        lambda documento: guardados.append(documento)
    )

    with pytest.raises(ValueError, match="bloqueado"):
        documento_service.cargar_documento(1, 5, "dpi.pdf", PDF)

    # No se registró nada en la base ni se escribió el archivo en disco.
    assert guardados == []
    assert list(tmp_path.iterdir()) == []


def test_solicitud_pendiente_si_acepta_documentos(monkeypatch, tmp_path):
    monkeypatch.setattr(documento_service, "CARPETA_DOCUMENTOS", str(tmp_path))
    monkeypatch.setattr(
        documento_service, "obtener_solicitud_por_id",
        solicitud_en_estado("pendiente")
    )
    monkeypatch.setattr(documento_service, "crear_documento", lambda documento: 7)
    monkeypatch.setattr(
        documento_service, "obtener_documento_por_id",
        lambda id_documento: {
            "id_documento": id_documento,
            "id_solicitud": 1,
            "nombre_archivo": "dpi.pdf",
            "tipo_archivo": "pdf",
            "fecha_carga": datetime(2026, 10, 31, 9, 0),
        }
    )

    resultado = documento_service.cargar_documento(1, 5, "dpi.pdf", PDF)

    assert resultado["id_documento"] == 7
    assert len(list(tmp_path.iterdir())) == 1


# ---------- Endpoint ----------

def test_endpoint_rechaza_la_carga_con_400(monkeypatch, tmp_path):
    monkeypatch.setattr(documento_service, "CARPETA_DOCUMENTOS", str(tmp_path))
    monkeypatch.setattr(
        documento_service, "obtener_solicitud_por_id",
        solicitud_en_estado("enviada")
    )
    app.dependency_overrides[get_current_user] = usuario_falso()

    response = client.post(
        "/api/documentos/solicitud/1",
        files={"archivo": ("dpi.pdf", PDF, "application/pdf")}
    )

    assert response.status_code == 400
    assert "bloqueado" in response.json()["detail"]


def test_otro_estudiante_recibe_403_y_no_se_entera_del_estado(monkeypatch, tmp_path):
    monkeypatch.setattr(documento_service, "CARPETA_DOCUMENTOS", str(tmp_path))
    monkeypatch.setattr(
        documento_service, "obtener_solicitud_por_id",
        solicitud_en_estado("enviada", id_estudiante=99)
    )
    app.dependency_overrides[get_current_user] = usuario_falso(id_usuario=5)

    response = client.post(
        "/api/documentos/solicitud/1",
        files={"archivo": ("dpi.pdf", PDF, "application/pdf")}
    )

    assert response.status_code == 403
