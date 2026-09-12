from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.models.estudiante import Estudiante
from app.schemas.estudiante import EstudianteRegistro
from app.services.estudiante_service import registrar_estudiante
from app.core.database import get_connection

router = APIRouter(
    prefix="/api/estudiantes",
    tags=["Estudiantes"]
)

class ActualizarPerfilSchema(BaseModel):
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    nivelEducativo: Optional[str] = None
    institucion: Optional[str] = None
    carrera: Optional[str] = None
    promedio: Optional[float] = None
    ingresoFamiliar: Optional[float] = None
    miembrosFamilia: Optional[int] = None
    ocupacionEncargado: Optional[str] = None
    tipoVivienda: Optional[str] = None
    dependientes: Optional[int] = None
    contactoEmergencia: Optional[str] = None


@router.post("/", status_code=201)
def registrar(data: EstudianteRegistro):
    try:
        estudiante = Estudiante(
            primer_nombre=data.primer_nombre,
            segundo_nombre=data.segundo_nombre,
            primer_apellido=data.primer_apellido,
            segundo_apellido=data.segundo_apellido,
            cui=data.cui,
            fecha_nacimiento=data.fecha_nacimiento,
            genero=data.genero,
            nacionalidad=data.nacionalidad,
            telefono=data.telefono,
            telefono_alternativo=data.telefono_alternativo,
            departamento=data.departamento,
            municipio=data.municipio,
            zona_aldea=data.zona_aldea,
            direccion_exacta=data.direccion_exacta,
            discapacidad=data.discapacidad,
            tipo_discapacidad=data.tipo_discapacidad,
            pueblo_pertenencia=data.pueblo_pertenencia,
            email=str(data.email),
            password_hash=""
        )

        id_estudiante = registrar_estudiante(
            estudiante=estudiante,
            password=data.password,
            datos_academicos=data.datos_academicos.model_dump(),
            datos_socioeconomicos=data.datos_socioeconomicos.model_dump(),
            contacto_emergencia=data.contacto_emergencia.model_dump()
        )

        return {
            "mensaje": "Estudiante registrado correctamente",
            "id_estudiante": id_estudiante
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception:
        raise HTTPException(status_code=500, detail="Ocurrió un error al registrar el estudiante.")


# -----------------------------------------------------------
# US-003: CONSULTAR Y ACTUALIZAR PERFIL EN POSTGRESQL
# -----------------------------------------------------------

@router.get("/{id_estudiante}")
def obtener_estudiante_por_id(id_estudiante: int):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id_estudiante, primer_nombre, segundo_nombre, primer_apellido, 
                       segundo_apellido, cui, fecha_nacimiento, genero, nacionalidad, 
                       telefono, direccion_exacta, email
                FROM estudiantes
                WHERE id_estudiante = %s;
            """, (id_estudiante,))
            est = cur.fetchone()

            if not est:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado en PostgreSQL")

            cur.execute("""
                SELECT nivel_educativo, establecimiento_educativo, universidad, carrera, promedio_notas, cum 
                FROM datos_academicos 
                WHERE id_estudiante = %s;
            """, (id_estudiante,))
            acad = cur.fetchone()

            cur.execute("""
                SELECT ingreso_familiar_mensual, numero_miembros_nucleo, ocupacion_encargado, tipo_vivienda, dependientes_economicos 
                FROM datos_socioeconomicos 
                WHERE id_estudiante = %s;
            """, (id_estudiante,))
            socio = cur.fetchone()

            cur.execute("""
                SELECT telefono_emergencia 
                FROM contacto_emergencia 
                WHERE id_estudiante = %s;
            """, (id_estudiante,))
            cont = cur.fetchone()

            return {
                "id_estudiante": est[0],
                "primer_nombre": est[1],
                "segundo_nombre": est[2],
                "primer_apellido": est[3],
                "segundo_apellido": est[4],
                "cui": est[5],
                "fecha_nacimiento": str(est[6]) if est[6] else None,
                "genero": est[7],
                "nacionalidad": est[8],
                "telefono": est[9],
                "direccion_exacta": est[10],
                "email": est[11],

                "nivel_educativo": acad[0] if acad else None,
                "institucion": (acad[2] or acad[1]) if acad else None,
                "carrera": acad[3] if acad else None,
                "promedio": float(acad[4] or acad[5]) if (acad and (acad[4] or acad[5])) else None,

                "ingreso_familiar_mensual": float(socio[0]) if (socio and socio[0]) else None,
                "numero_miembros_nucleo": socio[1] if socio else None,
                "ocupacion_encargado": socio[2] if socio else None,
                "tipo_vivienda": socio[3] if socio else None,
                "dependientes_economicos": socio[4] if socio else None,

                "telefono_emergencia": cont[0] if cont else None
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.put("/{id_estudiante}")
def actualizar_estudiante_por_id(id_estudiante: int, data: ActualizarPerfilSchema):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # 1. Actualizar tabla estudiantes
            campos_est = []
            valores_est = []
            if data.telefono is not None:
                campos_est.append("telefono = %s")
                valores_est.append(data.telefono)
            if data.direccion is not None:
                campos_est.append("direccion_exacta = %s")
                valores_est.append(data.direccion)

            if campos_est:
                valores_est.append(id_estudiante)
                cur.execute(f"UPDATE estudiantes SET {', '.join(campos_est)} WHERE id_estudiante = %s;", tuple(valores_est))

            # 2. Actualizar datos_academicos (comprobación por 1 en lugar de id_datos_academicos)
            cur.execute("SELECT 1 FROM datos_academicos WHERE id_estudiante = %s;", (id_estudiante,))
            if cur.fetchone():
                cur.execute("""
                    UPDATE datos_academicos 
                    SET nivel_educativo = COALESCE(%s, nivel_educativo),
                        universidad = COALESCE(%s, universidad),
                        establecimiento_educativo = COALESCE(%s, establecimiento_educativo),
                        carrera = COALESCE(%s, carrera),
                        promedio_notas = COALESCE(%s, promedio_notas)
                    WHERE id_estudiante = %s;
                """, (data.nivelEducativo, data.institucion, data.institucion, data.carrera, data.promedio, id_estudiante))
            else:
                cur.execute("""
                    INSERT INTO datos_academicos (id_estudiante, nivel_educativo, universidad, establecimiento_educativo, carrera, promedio_notas)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (id_estudiante, data.nivelEducativo, data.institucion, data.institucion, data.carrera, data.promedio))

            # 3. Actualizar datos_socioeconomicos
            cur.execute("SELECT 1 FROM datos_socioeconomicos WHERE id_estudiante = %s;", (id_estudiante,))
            if cur.fetchone():
                cur.execute("""
                    UPDATE datos_socioeconomicos
                    SET ingreso_familiar_mensual = COALESCE(%s, ingreso_familiar_mensual),
                        numero_miembros_nucleo = COALESCE(%s, numero_miembros_nucleo),
                        ocupacion_encargado = COALESCE(%s, ocupacion_encargado),
                        tipo_vivienda = COALESCE(%s, tipo_vivienda),
                        dependientes_economicos = COALESCE(%s, dependientes_economicos)
                    WHERE id_estudiante = %s;
                """, (data.ingresoFamiliar, data.miembrosFamilia, data.ocupacionEncargado, data.tipoVivienda, data.dependientes, id_estudiante))
            else:
                cur.execute("""
                    INSERT INTO datos_socioeconomicos (id_estudiante, ingreso_familiar_mensual, numero_miembros_nucleo, ocupacion_encargado, tipo_vivienda, dependientes_economicos)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (id_estudiante, data.ingresoFamiliar, data.miembrosFamilia, data.ocupacionEncargado, data.tipoVivienda, data.dependientes))

            # 4. Actualizar contacto_emergencia
            if data.contactoEmergencia:
                cur.execute("SELECT 1 FROM contacto_emergencia WHERE id_estudiante = %s;", (id_estudiante,))
                if cur.fetchone():
                    cur.execute("""
                        UPDATE contacto_emergencia 
                        SET telefono_emergencia = %s 
                        WHERE id_estudiante = %s;
                    """, (data.contactoEmergencia, id_estudiante))
                else:
                    cur.execute("""
                        INSERT INTO contacto_emergencia (id_estudiante, nombre_encargado, parentesco, telefono_emergencia)
                        VALUES (%s, %s, %s, %s);
                    """, (id_estudiante, "Encargado Principal", "Familiar", data.contactoEmergencia))

            conn.commit()
            return {"mensaje": "Perfil actualizado con éxito en PostgreSQL"}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()