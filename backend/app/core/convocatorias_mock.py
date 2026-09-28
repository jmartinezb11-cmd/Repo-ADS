from datetime import date

# --- MOCK temporal, mientras US-005 conecta con PostgreSQL ---
# Cuando Abraham termine US-005, esto se reemplaza por consultas reales
# a la base de datos. La lógica de US-007 (publicar) no cambia.

CONVOCATORIAS_DB = {
    1: {
        "id": 1,
        "titulo": "Beca Universitaria 2027",
        "descripcion": "Apoyo para estudiantes universitarios.",
        "fecha_apertura": date(2027, 1, 15),
        "fecha_cierre": date(2027, 3, 15),
        "requisitos": "Promedio mínimo de 80 puntos.",
        "estado": "borrador",
        "fecha_creacion": date(2026, 9, 1),
        "id_usuario_creador": 3,
    },
    2: {
        "id": 2,
        "titulo": "Beca Deportiva 2027",
        "descripcion": "Apoyo para estudiantes deportistas.",
        "fecha_apertura": date(2027, 2, 1),
        "fecha_cierre": date(2027, 4, 1),
        "requisitos": "Ser parte de un equipo representativo.",
        "estado": "publicada",
        "fecha_creacion": date(2026, 9, 1),
        "id_usuario_creador": 3,
    },
}