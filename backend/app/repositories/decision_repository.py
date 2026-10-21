from app.core.database import get_connection


def registrar_decision(
    id_solicitud: int,
    estado_nuevo: str,
    comentario: str | None,
    id_decisor: int,
    estados_permitidos: list[str]
) -> dict | None:

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # El filtro por estado hace que dos administradores no puedan
        # decidir la misma solicitud a la vez.
        query = """
            UPDATE solicitudes
            SET
                estado = %s,
                comentario_decision = %s,
                id_decisor = %s,
                fecha_decision = CURRENT_TIMESTAMP,
                fecha_ultima_actualizacion = CURRENT_TIMESTAMP
            WHERE id_solicitud = %s
              AND estado = ANY(%s)
            RETURNING
                id_solicitud,
                id_estudiante,
                id_convocatoria,
                estado,
                comentario_decision,
                id_decisor,
                fecha_decision;
        """

        cursor.execute(
            query,
            (
                estado_nuevo,
                comentario,
                id_decisor,
                id_solicitud,
                estados_permitidos,
            ),
        )

        fila = cursor.fetchone()

        if fila is None:
            connection.rollback()
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]
        solicitud = dict(zip(columnas, fila))

        connection.commit()

        return solicitud

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
