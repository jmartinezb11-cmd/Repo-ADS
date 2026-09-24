from app.core.database import get_connection
from app.models.convocatoria import Convocatoria


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