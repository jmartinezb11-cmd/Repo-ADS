
import pytest

from app.services import reporte_resultados_service


def test_reporte_con_resultados(monkeypatch):
    datos = [
        {"resultado": "aprobada"},
        {"resultado": "aprobada"},
        {"resultado": "rechazada"},
    ]

    monkeypatch.setattr(
        reporte_resultados_service,
        "listar_resultados",
        lambda id_convocatoria, estado: datos
    )

    reporte = reporte_resultados_service.generar_reporte_resultados()

    assert reporte["resumen"]["total_resueltas"] == 3
    assert reporte["resumen"]["aprobadas"] == 2
    assert reporte["resumen"]["rechazadas"] == 1
    assert reporte["resumen"]["porcentaje_aprobacion"] == 66.67


def test_reporte_sin_resultados(monkeypatch):
    monkeypatch.setattr(
        reporte_resultados_service,
        "listar_resultados",
        lambda id_convocatoria, estado: []
    )

    reporte = reporte_resultados_service.generar_reporte_resultados()

    assert reporte["resumen"]["total_resueltas"] == 0
    assert reporte["resumen"]["porcentaje_aprobacion"] == 0
    assert reporte["resultados"] == []


def test_estado_invalido():
    with pytest.raises(ValueError):
        reporte_resultados_service.generar_reporte_resultados(
            estado="pendiente"
        )


def test_convocatoria_inexistente(monkeypatch):
    monkeypatch.setattr(
        reporte_resultados_service,
        "obtener_convocatoria_por_id",
        lambda id_convocatoria: None
    )

    with pytest.raises(LookupError):
        reporte_resultados_service.generar_reporte_resultados(
            id_convocatoria=99999
        )


def test_filtros_reporte(monkeypatch):
    filtros_recibidos = {}

    monkeypatch.setattr(
        reporte_resultados_service,
        "obtener_convocatoria_por_id",
        lambda id_convocatoria: {"id_convocatoria": id_convocatoria}
    )

    def listar(id_convocatoria, estado):
        filtros_recibidos["id_convocatoria"] = id_convocatoria
        filtros_recibidos["estado"] = estado
        return [{"resultado": "aprobada"}]

    monkeypatch.setattr(
        reporte_resultados_service,
        "listar_resultados",
        listar
    )

    reporte = reporte_resultados_service.generar_reporte_resultados(
        id_convocatoria=1,
        estado="aprobada"
    )

    assert filtros_recibidos == {
        "id_convocatoria": 1,
        "estado": "aprobada"
    }
    assert reporte["resumen"]["aprobadas"] == 1
