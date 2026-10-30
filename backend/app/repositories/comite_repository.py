
from app.core.database import get_connection


def crear_comite_db(nombre_comite: str, descripcion: str | None):
    conexion = get_connection()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO comites (nombre_comite, descripcion)
                VALUES (%s, %s)
                RETURNING id_comite, nombre_comite, descripcion,
                          estado, fecha_creacion
                """,
                (nombre_comite, descripcion)
            )

            fila = cursor.fetchone()
            columnas = [columna[0] for columna in cursor.description]
            resultado = dict(zip(columnas, fila))

        conexion.commit()
        return resultado

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def obtener_comite_db(id_comite: int):
    conexion = get_connection()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_comite, nombre_comite, descripcion,
                       estado, fecha_creacion
                FROM comites
                WHERE id_comite = %s
                """,
                (id_comite,)
            )

            fila = cursor.fetchone()

            if fila is None:
                return None

            columnas = [columna[0] for columna in cursor.description]
            return dict(zip(columnas, fila))

    finally:
        conexion.close()


def obtener_usuario_para_comite_db(id_estudiante: int):
    conexion = get_connection()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_estudiante, primer_nombre,
                       primer_apellido, rol, estado_cuenta
                FROM estudiantes
                WHERE id_estudiante = %s
                """,
                (id_estudiante,)
            )

            fila = cursor.fetchone()

            if fila is None:
                return None

            columnas = [columna[0] for columna in cursor.description]
            return dict(zip(columnas, fila))

    finally:
        conexion.close()


def asignar_miembro_db(
    id_comite: int,
    id_estudiante: int,
    rol_comite: str
):
    conexion = get_connection()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO miembros_comite
                    (id_comite, id_estudiante, rol_comite)
                VALUES (%s, %s, %s)
                ON CONFLICT (id_comite, id_estudiante)
                DO NOTHING
                RETURNING id_miembro, id_comite,
                          id_estudiante, rol_comite,
                          fecha_asignacion
                """,
                (id_comite, id_estudiante, rol_comite)
            )

            fila = cursor.fetchone()

            if fila is None:
                conexion.rollback()
                raise ValueError(
                    "El usuario ya pertenece a este comité."
                )

            columnas = [columna[0] for columna in cursor.description]
            resultado = dict(zip(columnas, fila))

        conexion.commit()
        return resultado

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def obtener_integrantes_comite_db(id_comite: int):
    conexion = get_connection()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    e.id_estudiante AS id_integrante,
                    CONCAT_WS(
                        ' ',
                        e.primer_nombre,
                        e.segundo_nombre,
                        e.primer_apellido,
                        e.segundo_apellido
                    ) AS nombre,
                    mc.rol_comite AS rol
                FROM miembros_comite mc
                INNER JOIN estudiantes e
                    ON e.id_estudiante = mc.id_estudiante
                WHERE mc.id_comite = %s
                ORDER BY mc.id_miembro
                """,
                (id_comite,)
            )

            filas = cursor.fetchall()
            columnas = [
                columna[0]
                for columna in cursor.description
            ]

            return [
                dict(zip(columnas, fila))
                for fila in filas
            ]

    finally:
        conexion.close()

        
def listar_comites_db():
    conexion = get_connection()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT id_comite, nombre_comite,
                       descripcion, estado, fecha_creacion
                FROM comites
                ORDER BY nombre_comite
                """
            )

            filas = cursor.fetchall()
            columnas = [
                columna[0]
                for columna in cursor.description
            ]

            return [
                dict(zip(columnas, fila))
                for fila in filas
            ]

    finally:
        conexion.close()

