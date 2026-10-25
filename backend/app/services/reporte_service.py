from datetime import datetime

from fpdf import FPDF

from app.repositories.convocatoria_repository import obtener_convocatoria_por_id
from app.repositories.reporte_repository import (
    obtener_totales_por_estado,
    listar_solicitudes_para_reporte,
)


# US-026 - Generar reporte de solicitudes

def generar_reporte_solicitudes(
    id_convocatoria: int | None = None,
    estado: str | None = None
) -> dict:

    estado = (estado or "").strip().lower() or None

    if (
        id_convocatoria is not None
        and obtener_convocatoria_por_id(id_convocatoria) is None
    ):
        raise ValueError("Convocatoria no encontrada.")

    totales = obtener_totales_por_estado(id_convocatoria, estado)
    solicitudes = listar_solicitudes_para_reporte(id_convocatoria, estado)

    return {
        "filtros": {
            "id_convocatoria": id_convocatoria,
            "estado": estado,
        },
        "generado_en": datetime.now().isoformat(timespec="seconds"),
        "total": sum(fila["total"] for fila in totales),
        "por_estado": {fila["estado"]: fila["total"] for fila in totales},
        "solicitudes": solicitudes,
    }


def _texto(valor, maximo: int = 60) -> str:
    # Las fuentes base del PDF solo soportan latin-1 (cubre tildes y ñ).
    texto = "" if valor is None else str(valor)
    return texto[:maximo].encode("latin-1", "replace").decode("latin-1")


def _fecha(valor) -> str:
    if hasattr(valor, "strftime"):
        return valor.strftime("%d/%m/%Y")
    return _texto(valor, 10)


def generar_pdf_solicitudes(reporte: dict) -> bytes:
    pdf = FPDF(orientation="L")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _texto("Reporte de solicitudes"),
             new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, _texto(f"Generado: {reporte['generado_en']}"),
             new_x="LMARGIN", new_y="NEXT")

    filtros = reporte["filtros"]
    pdf.cell(
        0, 6,
        _texto(
            f"Filtros -> convocatoria: {filtros['id_convocatoria'] or 'todas'}"
            f" | estado: {filtros['estado'] or 'todos'}"
        ),
        new_x="LMARGIN", new_y="NEXT"
    )
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, _texto(f"Total de solicitudes: {reporte['total']}"),
             new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    for estado, cantidad in reporte["por_estado"].items():
        pdf.cell(0, 6, _texto(f"   {estado}: {cantidad}"),
                 new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    anchos = (15, 85, 70, 30, 30)
    encabezados = ("ID", "Convocatoria", "Estudiante", "Estado", "Fecha")

    pdf.set_font("Helvetica", "B", 10)
    for ancho, titulo in zip(anchos, encabezados):
        pdf.cell(ancho, 7, titulo, border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for fila in reporte["solicitudes"]:
        valores = (
            _texto(fila["id_solicitud"], 8),
            _texto(fila["convocatoria"], 45),
            _texto(fila["estudiante"], 38),
            _texto(fila["estado"], 15),
            _fecha(fila["fecha_creacion"]),
        )
        for ancho, valor in zip(anchos, valores):
            pdf.cell(ancho, 6, valor, border=1)
        pdf.ln()

    return bytes(pdf.output())
