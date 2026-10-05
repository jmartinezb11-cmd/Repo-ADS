from app.core.database import get_connection
from app.models.solicitud import Solicitud


def crear_solicitud(solicitud: Solicitud) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO solicitudes (
                id_estudiante,
                id_convocatoria,
                estado
            )
            VALUES (%s, %s, %s)
            RETURNING id_solicitud;
        """

        cursor.execute(
            query,
            (
                solicitud.id_estudiante,
                solicitud.id_convocatoria,
                solicitud.estado,
            ),
        )

        id_solicitud = cursor.fetchone()[0]

        connection.commit()

        return id_solicitud

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def obtener_solicitud_por_id(id_solicitud: int) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                id_solicitud,
                id_estudiante,
                id_convocatoria,
                estado,
                fecha_creacion,
                fecha_ultima_actualizacion
            FROM solicitudes
            WHERE id_solicitud = %s;
        """

        cursor.execute(query, (id_solicitud,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]
        return dict(zip(columnas, fila))

    finally:
        cursor.close()
        connection.close()


def existe_solicitud_duplicada(id_estudiante: int, id_convocatoria: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT 1
            FROM solicitudes
            WHERE id_estudiante = %s AND id_convocatoria = %s;
        """

        cursor.execute(query, (id_estudiante, id_convocatoria))
        return cursor.fetchone() is not None

    finally:
        cursor.close()
        connection.close()
