from app.core.database import get_connection
from app.models.evaluacion import Evaluacion


def crear_evaluacion(evaluacion: Evaluacion) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO evaluaciones (
                id_solicitud,
                id_evaluador,
                id_asignador
            )
            VALUES (%s, %s, %s)
            RETURNING id_evaluacion;
        """

        cursor.execute(
            query,
            (
                evaluacion.id_solicitud,
                evaluacion.id_evaluador,
                evaluacion.id_asignador,
            ),
        )

        id_evaluacion = cursor.fetchone()[0]

        connection.commit()

        return id_evaluacion

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def obtener_evaluacion_por_id(id_evaluacion: int) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                id_evaluacion,
                id_solicitud,
                id_evaluador,
                id_asignador,
                estado,
                fecha_asignacion
            FROM evaluaciones
            WHERE id_evaluacion = %s;
        """

        cursor.execute(query, (id_evaluacion,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]

        return dict(zip(columnas, fila))

    finally:
        cursor.close()
        connection.close()


def existe_evaluacion(id_solicitud: int, id_evaluador: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT 1
            FROM evaluaciones
            WHERE id_solicitud = %s
              AND id_evaluador = %s
            LIMIT 1;
        """

        cursor.execute(query, (id_solicitud, id_evaluador))

        return cursor.fetchone() is not None

    finally:
        cursor.close()
        connection.close()


def listar_evaluaciones_por_evaluador(id_evaluador: int) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                e.id_evaluacion,
                e.id_solicitud,
                c.titulo AS convocatoria,
                e.estado,
                e.fecha_asignacion
            FROM evaluaciones e
            JOIN solicitudes s ON s.id_solicitud = e.id_solicitud
            JOIN convocatorias c ON c.id_convocatoria = s.id_convocatoria
            WHERE e.id_evaluador = %s
            ORDER BY e.fecha_asignacion DESC;
        """

        cursor.execute(query, (id_evaluador,))
        filas = cursor.fetchall()

        columnas = [descripcion[0] for descripcion in cursor.description]

        return [dict(zip(columnas, fila)) for fila in filas]

    finally:
        cursor.close()
        connection.close()


def listar_solicitudes_por_estados(estados: list[str]) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                s.id_solicitud,
                e.primer_nombre || ' ' || e.primer_apellido AS estudiante,
                c.titulo AS convocatoria,
                s.estado
            FROM solicitudes s
            JOIN estudiantes e ON e.id_estudiante = s.id_estudiante
            JOIN convocatorias c ON c.id_convocatoria = s.id_convocatoria
            WHERE s.estado = ANY(%s)
            ORDER BY s.fecha_creacion DESC;
        """

        cursor.execute(query, (estados,))
        filas = cursor.fetchall()

        columnas = [descripcion[0] for descripcion in cursor.description]

        return [dict(zip(columnas, fila)) for fila in filas]

    finally:
        cursor.close()
        connection.close()


def listar_evaluadores_activos() -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                id_estudiante AS id_evaluador,
                primer_nombre || ' ' || primer_apellido AS nombre,
                email
            FROM estudiantes
            WHERE rol = 'evaluador'
              AND estado_cuenta <> 'inactivo'
            ORDER BY primer_nombre, primer_apellido;
        """

        cursor.execute(query)
        filas = cursor.fetchall()

        columnas = [descripcion[0] for descripcion in cursor.description]

        return [dict(zip(columnas, fila)) for fila in filas]

    finally:
        cursor.close()
        connection.close()