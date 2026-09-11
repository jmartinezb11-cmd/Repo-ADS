from fastapi import APIRouter, HTTPException

from app.models.estudiante import Estudiante
from app.schemas.estudiante import EstudianteRegistro
from app.services.estudiante_service import registrar_estudiante


router = APIRouter(
    prefix="/api/estudiantes",
    tags=["Estudiantes"]
)


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
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al registrar el estudiante."
        )



    