from app.core.database import get_connection
from app.models.convocatoria import Convocatoria


# =========================================================
# US-005 - Crear convocatoria
# =========================================================
def crear_convocatoria(convocatoria: Convocatoria) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO convocatorias (
                titulo,
                descripcion,
                tipo_beca,
                institucion,
                fecha_apertura,
                fecha_cierre,
                nivel_educativo,
                requisitos,
                monto_beneficio,
                cupos_disponibles,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_convocatoria;
        """

        cursor.execute(
            query,
            (
                convocatoria.titulo,
                convocatoria.descripcion,
                convocatoria.tipo_beca,
                convocatoria.institucion,
                convocatoria.fecha_apertura,
                convocatoria.fecha_cierre,
                convocatoria.nivel_educativo,
                convocatoria.requisitos,
                convocatoria.monto_beneficio,
                convocatoria.cupos_disponibles,
                convocatoria.estado,
            ),
        )

        id_convocatoria = cursor.fetchone()[0]

        connection.commit()

        return id_convocatoria

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


# =========================================================
# US-008 - Consultar convocatorias
# =========================================================
def obtener_convocatorias() -> list:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                id_convocatoria,
                titulo,
                descripcion,
                tipo_beca,
                institucion,
                fecha_apertura,
                fecha_cierre,
                nivel_educativo,
                requisitos,
                monto_beneficio,
                cupos_disponibles,
                estado,
                fecha_creacion,
                fecha_ultima_actualizacion
            FROM convocatorias
            ORDER BY fecha_creacion DESC;
        """

        cursor.execute(query)
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


def obtener_convocatoria_por_id(
    id_convocatoria: int
) -> dict | None:

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                id_convocatoria,
                titulo,
                descripcion,
                tipo_beca,
                institucion,
                fecha_apertura,
                fecha_cierre,
                nivel_educativo,
                requisitos,
                monto_beneficio,
                cupos_disponibles,
                estado,
                fecha_creacion,
                fecha_ultima_actualizacion
            FROM convocatorias
            WHERE id_convocatoria = %s;
        """

        cursor.execute(
            query,
            (id_convocatoria,)
        )

        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [
            descripcion[0]
            for descripcion in cursor.description
        ]

        return dict(zip(columnas, fila))

    finally:
        cursor.close()
        connection.close()


def listar_convocatorias() -> list[dict]:
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id_convocatoria,
                titulo,
                descripcion,
                fecha_apertura,
                fecha_cierre,
                estado
            FROM convocatorias
            ORDER BY fecha_creacion DESC
            """
        )

        filas = cursor.fetchall()

        return [
            {
                "id_convocatoria": fila[0],
                "titulo": fila[1],
                "descripcion": fila[2],
                "fecha_apertura": fila[3],
                "fecha_cierre": fila[4],
                "estado": fila[5]
            }
            for fila in filas
        ]

    finally:
        if cursor:
            cursor.close()

        connection.close()


def actualizar_estado_convocatoria(
    id_convocatoria: int,
    nuevo_estado: str
) -> bool:
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE convocatorias
            SET
                estado = %s,
                fecha_ultima_actualizacion = CURRENT_TIMESTAMP
            WHERE id_convocatoria = %s
            """,
            (nuevo_estado, id_convocatoria)
        )

        connection.commit()

        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        connection.close()


# =========================================================
# US-006 - Editar convocatoria
# =========================================================
def actualizar_convocatoria(
    id_convocatoria: int,
    datos: dict
) -> bool:

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            UPDATE convocatorias
            SET
                titulo = %s,
                descripcion = %s,
                tipo_beca = %s,
                institucion = %s,
                fecha_apertura = %s,
                fecha_cierre = %s,
                nivel_educativo = %s,
                requisitos = %s,
                monto_beneficio = %s,
                cupos_disponibles = %s,
                fecha_ultima_actualizacion = CURRENT_TIMESTAMP
            WHERE id_convocatoria = %s;
        """

        cursor.execute(
            query,
            (
                datos["titulo"],
                datos["descripcion"],
                datos["tipo_beca"],
                datos["institucion"],
                datos["fecha_apertura"],
                datos["fecha_cierre"],
                datos["nivel_educativo"],
                datos["requisitos"],
                datos.get("monto_beneficio"),
                datos.get("cupos_disponibles"),
                id_convocatoria,
            ),
        )

        actualizado = cursor.rowcount > 0

        connection.commit()

        return actualizado

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


# =========================================================
# US-007 - Publicar convocatoria
# =========================================================
def publicar_convocatoria(
    id_convocatoria: int
) -> dict | None:

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            UPDATE convocatorias
            SET
                estado = 'publicada',
                fecha_ultima_actualizacion = CURRENT_TIMESTAMP
            WHERE id_convocatoria = %s
              AND estado = 'borrador'
            RETURNING
                id_convocatoria,
                titulo,
                descripcion,
                tipo_beca,
                institucion,
                fecha_apertura,
                fecha_cierre,
                nivel_educativo,
                requisitos,
                monto_beneficio,
                cupos_disponibles,
                estado;
        """

        cursor.execute(
            query,
            (id_convocatoria,)
        )

        fila = cursor.fetchone()

        if fila is None:
            connection.rollback()
            return None

        columnas = [
            descripcion[0]
            for descripcion in cursor.description
        ]

        convocatoria = dict(zip(columnas, fila))

        connection.commit()

        return convocatoria

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()