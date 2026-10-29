
from app.core.database import get_connection


def listar_resultados(
    id_convocatoria: int | None = None,
    estado: str | None = None
) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                s.id_solicitud,
                s.id_convocatoria,
                c.titulo AS convocatoria,
                s.id_estudiante,
                e.primer_nombre || ' ' || e.primer_apellido
                    AS estudiante,
                s.estado AS resultado,
                s.comentario_decision,
                s.id_decisor,
                s.fecha_decision
            FROM solicitudes s
            INNER JOIN convocatorias c
                ON c.id_convocatoria = s.id_convocatoria
            INNER JOIN estudiantes e
                ON e.id_estudiante = s.id_estudiante
            WHERE s.estado IN ('aprobada', 'rechazada')
              AND (%s::int IS NULL OR s.id_convocatoria = %s)
              AND (%s::text IS NULL OR s.estado = %s)
            ORDER BY s.fecha_decision DESC NULLS LAST,
                     s.id_solicitud DESC;
        """

        cursor.execute(
            query,
            (
                id_convocatoria,
                id_convocatoria,
                estado,
                estado
            )
        )

        filas = cursor.fetchall()
        columnas = [
            descripcion[0]
            for descripcion in cursor.description
        ]

        return [
            dict(zip(columnas, fila))
            for fila in filas
        ]

    finally:
        cursor.close()
        connection.close()
