from fastapi import APIRouter, HTTPException

from app.models.convocatoria import Convocatoria
from app.schemas.convocatoria import ConvocatoriaCrear
from app.services.convocatoria_service import registrar_convocatoria


router = APIRouter(
    prefix="/api/convocatorias",
    tags=["Convocatorias"]
)


@router.post("/", status_code=201)
def crear(data: ConvocatoriaCrear):
    try:
        convocatoria = Convocatoria(
            titulo=data.titulo,
            descripcion=data.descripcion,
            tipo_beca=data.tipo_beca,
            institucion=data.institucion,
            fecha_apertura=data.fecha_apertura,
            fecha_cierre=data.fecha_cierre,
            nivel_educativo=data.nivel_educativo,
            requisitos=data.requisitos,
            monto_beneficio=data.monto_beneficio,
            cupos_disponibles=data.cupos_disponibles,
            estado="borrador"
        )

        id_convocatoria = registrar_convocatoria(convocatoria)

        return {
            "mensaje": "Convocatoria creada correctamente",
            "id_convocatoria": id_convocatoria,
            "estado": "borrador"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al crear la convocatoria."
        )