from app.core.database import get_connection


# Los filtros son opcionales: si llegan en None, no filtran nada.
FILTROS = """
    WHERE (%s::int IS NULL OR s.id_convocatoria = %s)
      AND (%s::text IS NULL OR s.estado = %s)
"""


def _parametros(id_convocatoria, estado):
    return (id_convocatoria, id_convocatoria, estado, estado)


def obtener_totales_por_estado(
    id_convocatoria: int | None,
    estado: str | None
) -> list[dict]:

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = f"""
            SELECT
                s.estado,
                COUNT(*) AS total
            FROM solicitudes s
            {FILTROS}
            GROUP BY s.estado
            ORDER BY s.estado;
        """

        cursor.execute(query, _parametros(id_convocatoria, estado))
        filas = cursor.fetchall()

        columnas = [descripcion[0] for descripcion in cursor.description]

        return [dict(zip(columnas, fila)) for fila in filas]

    finally:
        cursor.close()
        connection.close()


def listar_solicitudes_para_reporte(
    id_convocatoria: int | None,
    estado: str | None
) -> list[dict]:

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = f"""
            SELECT
                s.id_solicitud,
                s.id_convocatoria,
                c.titulo AS convocatoria,
                s.id_estudiante,
                e.primer_nombre || ' ' || e.primer_apellido AS estudiante,
                s.estado,
                s.fecha_creacion,
                s.fecha_ultima_actualizacion
            FROM solicitudes s
            INNER JOIN convocatorias c
                ON c.id_convocatoria = s.id_convocatoria
            INNER JOIN estudiantes e
                ON e.id_estudiante = s.id_estudiante
            {FILTROS}
            ORDER BY s.fecha_creacion DESC;
        """

        cursor.execute(query, _parametros(id_convocatoria, estado))
        filas = cursor.fetchall()

        columnas = [descripcion[0] for descripcion in cursor.description]

        return [dict(zip(columnas, fila)) for fila in filas]

    finally:
        cursor.close()
        connection.close()
