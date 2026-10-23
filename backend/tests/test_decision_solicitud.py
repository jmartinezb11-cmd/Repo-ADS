import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role
import app.api.routes.decisiones as decisiones_route
import app.services.decision_service as decision_service
from app.services.decision_service import SolicitudNoEncontrada


def usuario_falso(rol: Role, id_usuario: int = 9):
    def _override():
        return {"id": id_usuario, "nombre": "Usuario de prueba", "rol": rol}
    return _override


client = TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_overrides():
    yield
    app.dependency_overrides.clear()


# ---------- Endpoint ----------

def test_admin_puede_aprobar(monkeypatch):
    def fake(id_solicitud, decision, comentario, id_decisor):
        return {
            "id_solicitud": id_solicitud,
            "estado": decision,
            "id_decisor": id_decisor,
        }

    monkeypatch.setattr(decisiones_route, "procesar_decision", fake)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.patch(
        "/api/solicitudes/1/decision",
        json={"decision": "aprobada"}
    )

    assert response.status_code == 200
    assert response.json()["solicitud"]["estado"] == "aprobada"
    assert response.json()["solicitud"]["id_decisor"] == 9


@pytest.mark.parametrize("rol", [Role.ESTUDIANTE, Role.EVALUADOR])
def test_otros_roles_no_pueden_decidir(rol):
    app.dependency_overrides[get_current_user] = usuario_falso(rol)

    response = client.patch(
        "/api/solicitudes/1/decision",
        json={"decision": "aprobada"}
    )

    assert response.status_code == 403


def test_decision_invalida_da_422():
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.patch(
        "/api/solicitudes/1/decision",
        json={"decision": "quizas"}
    )

    assert response.status_code == 422


def test_solicitud_inexistente_da_404(monkeypatch):
    def fake(*args):
        raise SolicitudNoEncontrada("Solicitud no encontrada.")

    monkeypatch.setattr(decisiones_route, "procesar_decision", fake)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.patch(
        "/api/solicitudes/999/decision",
        json={"decision": "aprobada"}
    )

    assert response.status_code == 404


def test_regla_de_negocio_incumplida_da_400(monkeypatch):
    def fake(*args):
        raise ValueError("Esta solicitud ya fue resuelta.")

    monkeypatch.setattr(decisiones_route, "procesar_decision", fake)
    app.dependency_overrides[get_current_user] = usuario_falso(Role.ADMINISTRADOR)

    response = client.patch(
        "/api/solicitudes/1/decision",
        json={"decision": "aprobada"}
    )

    assert response.status_code == 400


# ---------- Service ----------

def test_rechazo_sin_motivo_da_error():
    with pytest.raises(ValueError):
        decision_service.procesar_decision(1, "rechazada", "   ", 9)


def test_solicitud_inexistente_en_service(monkeypatch):
    monkeypatch.setattr(
        decision_service, "obtener_solicitud_por_id", lambda id_solicitud: None
    )

    with pytest.raises(SolicitudNoEncontrada):
        decision_service.procesar_decision(999, "aprobada", None, 9)


@pytest.mark.parametrize("estado", ["aprobada", "rechazada"])
def test_no_se_decide_una_solicitud_ya_resuelta(monkeypatch, estado):
    monkeypatch.setattr(
        decision_service, "obtener_solicitud_por_id",
        lambda id_solicitud: {"id_solicitud": id_solicitud, "estado": estado}
    )

    with pytest.raises(ValueError, match="ya fue resuelta"):
        decision_service.procesar_decision(1, "aprobada", None, 9)


def test_no_se_decide_una_solicitud_pendiente(monkeypatch):
    monkeypatch.setattr(
        decision_service, "obtener_solicitud_por_id",
        lambda id_solicitud: {"id_solicitud": id_solicitud, "estado": "pendiente"}
    )

    with pytest.raises(ValueError, match="No se puede decidir"):
        decision_service.procesar_decision(1, "aprobada", None, 9)


def test_solicitud_enviada_se_puede_rechazar(monkeypatch):
    monkeypatch.setattr(
        decision_service, "obtener_solicitud_por_id",
        lambda id_solicitud: {"id_solicitud": id_solicitud, "estado": "enviada"}
    )
    monkeypatch.setattr(
        decision_service, "registrar_decision",
        lambda id_solicitud, estado, comentario, id_decisor, permitidos: {
            "id_solicitud": id_solicitud,
            "estado": estado,
            "comentario_decision": comentario,
        }
    )

    resultado = decision_service.procesar_decision(
        1, "rechazada", "Documentación incompleta", 9
    )

    assert resultado["estado"] == "rechazada"
    assert resultado["comentario_decision"] == "Documentación incompleta"


def test_cambio_de_estado_concurrente(monkeypatch):
    monkeypatch.setattr(
        decision_service, "obtener_solicitud_por_id",
        lambda id_solicitud: {"id_solicitud": id_solicitud, "estado": "enviada"}
    )
    monkeypatch.setattr(
        decision_service, "registrar_decision", lambda *args: None
    )

    with pytest.raises(ValueError, match="cambió de estado"):
        decision_service.procesar_decision(1, "aprobada", None, 9)
