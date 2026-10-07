from app.core.database import get_connection
from app.models.documento import Documento


def crear_documento(documento: Documento) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO documentos (
                id_solicitud,
                nombre_archivo,
                tipo_archivo,
                ruta_archivo
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id_documento;
        """

        cursor.execute(
            query,
            (
                documento.id_solicitud,
                documento.nombre_archivo,
                documento.tipo_archivo,
                documento.ruta_archivo,
            ),
        )

        id_documento = cursor.fetchone()[0]

        connection.commit()

        return id_documento

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def listar_documentos_por_solicitud(id_solicitud: int) -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                id_documento,
                id_solicitud,
                nombre_archivo,
                tipo_archivo,
                fecha_carga
            FROM documentos
            WHERE id_solicitud = %s
            ORDER BY fecha_carga DESC;
        """

        cursor.execute(query, (id_solicitud,))
        filas = cursor.fetchall()

        columnas = [descripcion[0] for descripcion in cursor.description]

        return [dict(zip(columnas, fila)) for fila in filas]

    finally:
        cursor.close()
        connection.close()


def obtener_documento_por_id(id_documento: int) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                id_documento,
                id_solicitud,
                nombre_archivo,
                tipo_archivo,
                ruta_archivo,
                fecha_carga
            FROM documentos
            WHERE id_documento = %s;
        """

        cursor.execute(query, (id_documento,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]

        return dict(zip(columnas, fila))

    finally:
        cursor.close()
        connection.close()