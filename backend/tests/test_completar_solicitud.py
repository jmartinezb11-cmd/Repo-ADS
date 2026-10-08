from fastapi.testclient import TestClient

from app.main import app
from app.core.deps import get_current_user
from app.core.roles import Role
import app.api.routes.solicitudes as solicitudes_route


client = TestClient(app)


def usuario_estudiante(id_usuario: int = 1):
    def _override():
        return {
            "id": id_usuario,
            "nombre": "Estudiante Demo",
            "rol": Role.ESTUDIANTE
        }

    return _override


def datos_validos():
    return {
        "motivacion": (
            "Deseo obtener esta beca para continuar con mis "
            "estudios universitarios."
        ),
        "situacion_economica": (
            "Mi familia cuenta con recursos económicos limitados "
            "para cubrir mis estudios."
        ),
        "ingresos_familiares": 3500.00,
        "integrantes_hogar": 5,
        "dependientes_economicos": 3,
        "ocupacion_responsable": "Comerciante",
        "institucion_educativa": (
            "Universidad de San Carlos de Guatemala"
        ),
        "carrera_area": "Ingeniería en Sistemas",
        "grado_semestre": "Quinto semestre",
        "promedio_academico": 82.50,
        "meta_academica": (
            "Finalizar mi carrera universitaria y desarrollarme "
            "profesionalmente."
        )
    }


def test_estudiante_puede_completar_su_solicitud(monkeypatch):
    def fake_completar(id_solicitud, id_estudiante, datos):
        return {
            "id_detalle": 1,
            "id_solicitud": id_solicitud,
            "motivacion": datos.motivacion,
            "estado_prueba": "completada"
        }

    monkeypatch.setattr(
        solicitudes_route,
        "completar_solicitud",
        fake_completar
    )

    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    response = client.put(
        "/api/solicitudes/1/completar",
        json=datos_validos()
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["mensaje"] == (
        "Solicitud completada correctamente"
    )
    assert response.json()["detalle"]["id_solicitud"] == 1


def test_estudiante_no_puede_modificar_solicitud_ajena(monkeypatch):
    def fake_completar(id_solicitud, id_estudiante, datos):
        raise PermissionError(
            "No tienes permiso para modificar esta solicitud."
        )

    monkeypatch.setattr(
        solicitudes_route,
        "completar_solicitud",
        fake_completar
    )

    app.dependency_overrides[get_current_user] = usuario_estudiante(2)

    response = client.put(
        "/api/solicitudes/1/completar",
        json=datos_validos()
    )

    app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "No tienes permiso para modificar esta solicitud."
    )


def test_solicitud_inexistente_da_error(monkeypatch):
    def fake_completar(id_solicitud, id_estudiante, datos):
        raise ValueError("Solicitud no encontrada.")

    monkeypatch.setattr(
        solicitudes_route,
        "completar_solicitud",
        fake_completar
    )

    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    response = client.put(
        "/api/solicitudes/999999/completar",
        json=datos_validos()
    )

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["detail"] == "Solicitud no encontrada."


def test_dependientes_no_pueden_superar_integrantes(monkeypatch):
    def fake_completar(id_solicitud, id_estudiante, datos):
        if datos.dependientes_economicos > datos.integrantes_hogar:
            raise ValueError(
                "Los dependientes económicos no pueden superar "
                "el número de integrantes del hogar."
            )

    monkeypatch.setattr(
        solicitudes_route,
        "completar_solicitud",
        fake_completar
    )

    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    datos = datos_validos()
    datos["integrantes_hogar"] = 4
    datos["dependientes_economicos"] = 8

    response = client.put(
        "/api/solicitudes/1/completar",
        json=datos
    )

    app.dependency_overrides.clear()

    assert response.status_code == 400


def test_promedio_fuera_de_rango_es_rechazado():
    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    datos = datos_validos()
    datos["promedio_academico"] = 150

    response = client.put(
        "/api/solicitudes/1/completar",
        json=datos
    )

    app.dependency_overrides.clear()

    assert response.status_code == 422


def test_ingresos_negativos_son_rechazados():
    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    datos = datos_validos()
    datos["ingresos_familiares"] = -100

    response = client.put(
        "/api/solicitudes/1/completar",
        json=datos
    )

    app.dependency_overrides.clear()

    assert response.status_code == 422


def test_motivacion_vacia_es_rechazada():
    app.dependency_overrides[get_current_user] = usuario_estudiante(1)

    datos = datos_validos()
    datos["motivacion"] = ""

    response = client.put(
        "/api/solicitudes/1/completar",
        json=datos
    )

    app.dependency_overrides.clear()

    assert response.status_code == 422