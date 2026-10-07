from datetime import date

# --- MOCK temporal, mientras US-014 (Cargar documentación) se conecta ---
# Cuando Josué Nehemías termine US-014, esto se reemplaza por consultas
# reales en documento_repository.py. La lógica de validación no cambia.

DOCUMENTOS_DB = {
    1: {
        "id_documento": 1,
        "id_solicitud": 1,
        "nombre_archivo": "constancia_estudios.pdf",
        "tipo_documento": "constancia",
        "estado_validacion": "pendiente",
        "comentario_validacion": None,
        "fecha_carga": date(2026, 9, 10),
    },
    2: {
        "id_documento": 2,
        "id_solicitud": 1,
        "nombre_archivo": "dpi.pdf",
        "tipo_documento": "identificacion",
        "estado_validacion": "aprobado",
        "comentario_validacion": "Documento legible y vigente.",
        "fecha_carga": date(2026, 9, 10),
    },
}
