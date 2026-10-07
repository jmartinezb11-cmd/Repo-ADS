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

# US-011 - Completar solicitud

def guardar_detalle_solicitud(detalle) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO detalle_solicitudes (
                id_solicitud,
                motivacion,
                situacion_economica,
                ingresos_familiares,
                integrantes_hogar,
                dependientes_economicos,
                ocupacion_responsable,
                institucion_educativa,
                carrera_area,
                grado_semestre,
                promedio_academico,
                meta_academica,
                fecha_actualizacion
            )
            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                CURRENT_TIMESTAMP
            )
            ON CONFLICT (id_solicitud)
            DO UPDATE SET
                motivacion = EXCLUDED.motivacion,
                situacion_economica = EXCLUDED.situacion_economica,
                ingresos_familiares = EXCLUDED.ingresos_familiares,
                integrantes_hogar = EXCLUDED.integrantes_hogar,
                dependientes_economicos = EXCLUDED.dependientes_economicos,
                ocupacion_responsable = EXCLUDED.ocupacion_responsable,
                institucion_educativa = EXCLUDED.institucion_educativa,
                carrera_area = EXCLUDED.carrera_area,
                grado_semestre = EXCLUDED.grado_semestre,
                promedio_academico = EXCLUDED.promedio_academico,
                meta_academica = EXCLUDED.meta_academica,
                fecha_actualizacion = CURRENT_TIMESTAMP
            RETURNING id_detalle;
        """

        cursor.execute(
            query,
            (
                detalle.id_solicitud,
                detalle.motivacion,
                detalle.situacion_economica,
                detalle.ingresos_familiares,
                detalle.integrantes_hogar,
                detalle.dependientes_economicos,
                detalle.ocupacion_responsable,
                detalle.institucion_educativa,
                detalle.carrera_area,
                detalle.grado_semestre,
                detalle.promedio_academico,
                detalle.meta_academica,
            ),
        )

        id_detalle = cursor.fetchone()[0]

        # También actualizamos la fecha de la solicitud principal.
        cursor.execute(
            """
            UPDATE solicitudes
            SET fecha_ultima_actualizacion = CURRENT_TIMESTAMP
            WHERE id_solicitud = %s;
            """,
            (detalle.id_solicitud,),
        )

        connection.commit()
        return id_detalle

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def obtener_detalle_solicitud(id_solicitud: int) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                id_detalle,
                id_solicitud,
                motivacion,
                situacion_economica,
                ingresos_familiares,
                integrantes_hogar,
                dependientes_economicos,
                ocupacion_responsable,
                institucion_educativa,
                carrera_area,
                grado_semestre,
                promedio_academico,
                meta_academica,
                fecha_actualizacion
            FROM detalle_solicitudes
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