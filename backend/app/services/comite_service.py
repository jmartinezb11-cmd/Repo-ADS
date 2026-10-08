# Servicio con MOCK para US-023: Consultar comité

MOCK_COMITE = {
    "id_comite": 101,
    "nombre_comite": "Comité Evaluador de Proyectos 2026",
    "integrantes": [
        {
            "id_integrante": 1,
            "nombre": "Dr. Carlos Mendoza",
            "rol": "Presidente",
            "asignaciones": ["Evaluación Convocatoria A1", "Revisión Final"]
        },
        {
            "id_integrante": 2,
            "nombre": "Ing. Ana Lucía Morales",
            "rol": "Evaluador Senior",
            "asignaciones": ["Evaluación Propuestas US-021"]
        },
        {
            "id_integrante": 3,
            "nombre": "Lic. Luis González",
            "rol": "Secretario",
            "asignaciones": ["Control de actas y seguimiento"]
        }
    ]
}

def obtener_integrantes_comite_mock(id_comite: int):
    # Cuando desbloqueen la US-21 o la base de datos, aquí se hará la consulta real
    return MOCK_COMITE