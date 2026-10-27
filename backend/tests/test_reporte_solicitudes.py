import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role
import app.api.routes.reportes as reportes_route
import app.services.reporte_service as reporte_service


def usuario_falso(rol: Role):
    def _override():
        return {"id": 1, "nombre": "Usuario de prueba", "rol": rol}
    return _override


def reporte_falso():
    return {
        "filtros": {"id_convocatoria": None, "estado": None},
        "generado_en": "2026-10-21T10:00:00",
        "total": 1,
        "por_estado": {"pendiente": 1},
        "solicitudes": [{
            "id_solicitud": 1,
            "id_convocatoria": 1,
            "convocatoria": "Beca Universitaria 2027",
            "id_estudiante": 5,
            "estudiante": "María Pérez",
            "estado": "pendiente",
            "fecha_creacion": datetime(2026, 10, 20, 9, 0),
            "fecha_ultima_actualizacion": datetime(2026, 10, 20, 9, 0),
        }],
    }


client = TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_overrides():
    yield
    app.dependency_overrides.clear()


# ---------- Endpoints ----------

def test_admin_obtiene_reporte_json(monkeypatch):
    monkeypatch.setattr(
        reportes_route, "generar_reporte_solicitudes",
        lambda id_convocatoria, estado: reporte_falso()
    )
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.get("/api/reportes/solicitudes")

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["por_estado"] == {"pendiente": 1}


def test_filtros_llegan_al_service(monkeypatch):
    recibido = {}

    def fake(id_convocatoria, estado):
        recibido["id_convocatoria"] = id_convocatoria
        recibido["estado"] = estado
        return reporte_falso()

    monkeypatch.setattr(reportes_route, "generar_reporte_solicitudes", fake)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    client.get("/api/reportes/solicitudes?id_convocatoria=3&estado=pendiente")

    assert recibido == {"id_convocatoria": 3, "estado": "pendiente"}


def test_estudiante_no_puede_ver_reporte():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)
    assert client.get("/api/reportes/solicitudes").status_code == 403


def test_evaluador_no_puede_ver_reporte():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.EVALUADOR)
    assert client.get("/api/reportes/solicitudes").status_code == 403


def test_convocatoria_inexistente_da_404(monkeypatch):
    def fake(id_convocatoria, estado):
        raise ValueError("Convocatoria no encontrada.")

    monkeypatch.setattr(reportes_route, "generar_reporte_solicitudes", fake)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.get("/api/reportes/solicitudes?id_convocatoria=999")

    assert response.status_code == 404


def test_admin_descarga_pdf(monkeypatch):
    monkeypatch.setattr(
        reportes_route, "generar_reporte_solicitudes",
        lambda id_convocatoria, estado: reporte_falso()
    )
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.get("/api/reportes/solicitudes/pdf")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_estudiante_no_puede_descargar_pdf():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ESTUDIANTE)
    assert client.get("/api/reportes/solicitudes/pdf").status_code == 403


# ---------- Service ----------

def test_service_suma_totales_por_estado(monkeypatch):
    monkeypatch.setattr(
        reporte_service, "obtener_totales_por_estado",
        lambda id_convocatoria, estado: [
            {"estado": "aprobada", "total": 2},
            {"estado": "pendiente", "total": 3},
        ]
    )
    monkeypatch.setattr(
        reporte_service, "listar_solicitudes_para_reporte",
        lambda id_convocatoria, estado: []
    )

    reporte = reporte_service.generar_reporte_solicitudes()

    assert reporte["total"] == 5
    assert reporte["por_estado"] == {"aprobada": 2, "pendiente": 3}


def test_service_convocatoria_inexistente(monkeypatch):
    monkeypatch.setattr(
        reporte_service, "obtener_convocatoria_por_id",
        lambda id_convocatoria: None
    )

    with pytest.raises(ValueError):
        reporte_service.generar_reporte_solicitudes(id_convocatoria=999)


def test_service_normaliza_el_estado(monkeypatch):
    recibido = {}

    def fake_totales(id_convocatoria, estado):
        recibido["estado"] = estado
        return []

    monkeypatch.setattr(reporte_service, "obtener_totales_por_estado", fake_totales)
    monkeypatch.setattr(
        reporte_service, "listar_solicitudes_para_reporte",
        lambda id_convocatoria, estado: []
    )

    reporte_service.generar_reporte_solicitudes(estado="  PENDIENTE ")

    assert recibido["estado"] == "pendiente"


def test_pdf_soporta_tildes_y_enie():
    contenido = reporte_service.generar_pdf_solicitudes(reporte_falso())
    assert contenido.startswith(b"%PDF")
