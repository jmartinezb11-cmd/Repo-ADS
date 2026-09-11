from app.core.database import get_connection
from app.models.estudiante import Estudiante


def existe_estudiante_por_email(email: str) -> bool:
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM estudiantes
            WHERE email = %s
            LIMIT 1
            """,
            (email,)
        )

        return cursor.fetchone() is not None

    finally:
        if cursor:
            cursor.close()

        connection.close()


def existe_estudiante_por_cui(cui: str) -> bool:
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM estudiantes
            WHERE cui = %s
            LIMIT 1
            """,
            (cui,)
        )

        return cursor.fetchone() is not None

    finally:
        if cursor:
            cursor.close()

        connection.close()


def crear_estudiante_completo(
    estudiante: Estudiante,
    datos_academicos: dict,
    datos_socioeconomicos: dict,
    contacto_emergencia: dict
) -> int:

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        # ==========================================
        # 1. INSERTAR ESTUDIANTE
        # ==========================================

        cursor.execute(
            """
            INSERT INTO estudiantes (
                primer_nombre,
                segundo_nombre,
                primer_apellido,
                segundo_apellido,
                cui,
                fecha_nacimiento,
                genero,
                nacionalidad,
                telefono,
                telefono_alternativo,
                departamento,
                municipio,
                zona_aldea,
                direccion_exacta,
                discapacidad,
                tipo_discapacidad,
                pueblo_pertenencia,
                email,
                password_hash
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING id_estudiante
            """,
            (
                estudiante.primer_nombre,
                estudiante.segundo_nombre,
                estudiante.primer_apellido,
                estudiante.segundo_apellido,
                estudiante.cui,
                estudiante.fecha_nacimiento,
                estudiante.genero,
                estudiante.nacionalidad,
                estudiante.telefono,
                estudiante.telefono_alternativo,
                estudiante.departamento,
                estudiante.municipio,
                estudiante.zona_aldea,
                estudiante.direccion_exacta,
                estudiante.discapacidad,
                estudiante.tipo_discapacidad,
                estudiante.pueblo_pertenencia,
                estudiante.email,
                estudiante.password_hash
            )
        )

        id_estudiante = cursor.fetchone()[0]

        # ==========================================
        # 2. DATOS ACADÉMICOS
        # ==========================================

        cursor.execute(
            """
            INSERT INTO datos_academicos (
                id_estudiante,
                nivel_educativo,
                establecimiento_educativo,
                grado_actual,
                jornada,
                sector,
                promedio_notas,
                especialidad,
                universidad,
                facultad_escuela,
                carrera,
                anio_semestre_actual,
                carnet_universitario,
                cum,
                creditos_aprobados,
                modalidad
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """,
            (
                id_estudiante,
                datos_academicos.get("nivel_educativo"),
                datos_academicos.get("establecimiento_educativo"),
                datos_academicos.get("grado_actual"),
                datos_academicos.get("jornada"),
                datos_academicos.get("sector"),
                datos_academicos.get("promedio_notas"),
                datos_academicos.get("especialidad"),
                datos_academicos.get("universidad"),
                datos_academicos.get("facultad_escuela"),
                datos_academicos.get("carrera"),
                datos_academicos.get("anio_semestre_actual"),
                datos_academicos.get("carnet_universitario"),
                datos_academicos.get("cum"),
                datos_academicos.get("creditos_aprobados"),
                datos_academicos.get("modalidad")
            )
        )

        # ==========================================
        # 3. DATOS SOCIOECONÓMICOS
        # ==========================================

        cursor.execute(
            """
            INSERT INTO datos_socioeconomicos (
                id_estudiante,
                ingreso_familiar_mensual,
                numero_miembros_nucleo,
                ocupacion_padre,
                ocupacion_madre,
                ocupacion_encargado,
                tipo_vivienda,
                dependientes_economicos
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """,
            (
                id_estudiante,
                datos_socioeconomicos.get("ingreso_familiar_mensual"),
                datos_socioeconomicos.get("numero_miembros_nucleo"),
                datos_socioeconomicos.get("ocupacion_padre"),
                datos_socioeconomicos.get("ocupacion_madre"),
                datos_socioeconomicos.get("ocupacion_encargado"),
                datos_socioeconomicos.get("tipo_vivienda"),
                datos_socioeconomicos.get("dependientes_economicos")
            )
        )

        # ==========================================
        # 4. CONTACTO DE EMERGENCIA
        # ==========================================

        cursor.execute(
            """
            INSERT INTO contacto_emergencia (
                id_estudiante,
                nombre_encargado,
                parentesco,
                telefono_emergencia
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                id_estudiante,
                contacto_emergencia.get("nombre_encargado"),
                contacto_emergencia.get("parentesco"),
                contacto_emergencia.get("telefono_emergencia")
            )
        )

        # Si las 4 inserciones funcionaron:
        connection.commit()

        return id_estudiante

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        connection.close()


def obtener_estudiante_por_email(email: str) -> dict | None:
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id_estudiante,
                primer_nombre,
                primer_apellido,
                email,
                password_hash,
                estado_cuenta
            FROM estudiantes
            WHERE email = %s
            LIMIT 1
            """,
            (email,)
        )

        fila = cursor.fetchone()

        if fila is None:
            return None

        return {
            "id_estudiante": fila[0],
            "primer_nombre": fila[1],
            "primer_apellido": fila[2],
            "email": fila[3],
            "password_hash": fila[4],
            "estado_cuenta": fila[5]
        }

    finally:
        if cursor:
            cursor.close()

        connection.close()        