import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role
import app.api.routes.documentos as documentos_route
from app.services import documento_service
from app.services.documento_service import RecursoNoEncontrado


def usuario_falso(rol: Role, id_usuario: int = 7):
    def _override():
        return {"id": id_usuario, "nombre": "Usuario de prueba", "rol": rol}
    return _override


client = TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_overrides():
    yield
    app.dependency_overrides.clear()


# ---------- Endpoints ----------

def test_evaluador_puede_aprobar_documento(monkeypatch):
    def fake(id_documento, estado, comentario, id_validador):
        return {
            "id_documento": id_documento,
            "estado_validacion": estado,
            "comentario_validacion": comentario,
            "id_validador": id_validador,
        }

    monkeypatch.setattr(documentos_route, "procesar_validacion", fake)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)

    response = client.patch(
        "/api/documentos/1/validar",
        json={"estado_validacion": "aprobado"}
    )

    assert response.status_code == 200
    assert response.json()["documento"]["estado_validacion"] == "aprobado"
    assert response.json()["documento"]["id_validador"] == 7


def test_estudiante_no_puede_validar():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)

    response = client.patch(
        "/api/documentos/1/validar",
        json={"estado_validacion": "aprobado"}
    )

    assert response.status_code == 403


def test_documento_inexistente_da_404(monkeypatch):
    def fake(*args):
        raise RecursoNoEncontrado("Documento no encontrado.")

    monkeypatch.setattr(documentos_route, "procesar_validacion", fake)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)

    response = client.patch(
        "/api/documentos/999/validar",
        json={"estado_validacion": "aprobado"}
    )

    assert response.status_code == 404


def test_documento_ya_procesado_da_400(monkeypatch):
    def fake(*args):
        raise ValueError("Este documento ya fue validado o rechazado.")

    monkeypatch.setattr(documentos_route, "procesar_validacion", fake)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)

    response = client.patch(
        "/api/documentos/1/validar",
        json={"estado_validacion": "aprobado"}
    )

    assert response.status_code == 400


def test_estado_invalido_da_422():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)

    response = client.patch(
        "/api/documentos/1/validar",
        json={"estado_validacion": "no_valido"}
    )

    assert response.status_code == 422


def test_evaluador_puede_listar_documentos_para_revision(monkeypatch):
    def fake(id_solicitud):
        return [{
            "id_documento": 1,
            "id_solicitud": id_solicitud,
            "nombre_archivo": "dpi.pdf",
            "tipo_archivo": "pdf",
            "fecha_carga": datetime(2026, 10, 8, 10, 0),
            "estado_validacion": "pendiente",
            "comentario_validacion": None,
            "fecha_validacion": None,
        }]

    monkeypatch.setattr(documentos_route, "listar_para_revision", fake)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)

    response = client.get("/api/documentos/revision/solicitud/1")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["estado_validacion"] == "pendiente"


def test_estudiante_no_puede_revisar_documentos():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)

    response = client.get("/api/documentos/revision/solicitud/1")

    assert response.status_code == 403


def test_evaluador_puede_abrir_el_pdf(monkeypatch, tmp_path):
    archivo = tmp_path / "doc.pdf"
    archivo.write_bytes(b"%PDF-1.4 prueba")

    monkeypatch.setattr(
        documentos_route,
        "obtener_ruta_archivo",
        lambda id_documento: (str(archivo), "doc.pdf")
    )
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)

    response = client.get("/api/documentos/1/archivo")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


# ---------- Reglas del service ----------

def test_estado_invalido_en_service():
    with pytest.raises(ValueError):
        documento_service.procesar_validacion(1, "otro", None, 7)


def test_rechazo_sin_comentario_da_error():
    with pytest.raises(ValueError):
        documento_service.procesar_validacion(1, "rechazado", "   ", 7)


def test_service_documento_inexistente(monkeypatch):
    monkeypatch.setattr(
        documento_service, "obtener_documento_por_id", lambda id_documento: None
    )

    with pytest.raises(RecursoNoEncontrado):
        documento_service.procesar_validacion(999, "aprobado", None, 7)


def test_service_documento_ya_procesado(monkeypatch):
    monkeypatch.setattr(
        documento_service, "obtener_documento_por_id",
        lambda id_documento: {"id_documento": id_documento}
    )
    monkeypatch.setattr(
        documento_service, "validar_documento", lambda *args: None
    )

    with pytest.raises(ValueError):
        documento_service.procesar_validacion(1, "aprobado", None, 7)


def test_service_rechaza_documento_pendiente(monkeypatch):
    monkeypatch.setattr(
        documento_service, "obtener_documento_por_id",
        lambda id_documento: {"id_documento": id_documento}
    )
    monkeypatch.setattr(
        documento_service, "validar_documento",
        lambda id_documento, estado, comentario, id_validador: {
            "id_documento": id_documento,
            "estado_validacion": estado,
            "comentario_validacion": comentario,
        }
    )

    resultado = documento_service.procesar_validacion(
        1, "rechazado", "Ilegible", 7
    )

    assert resultado["estado_validacion"] == "rechazado"
    assert resultado["comentario_validacion"] == "Ilegible"
