from fastapi import APIRouter, HTTPException, Depends

from app.core.deps import require_role
from app.core.roles import Role

from app.models.convocatoria import Convocatoria
from app.schemas.convocatoria import (
    ConvocatoriaCrear,
    ConvocatoriaResumen,
    CerrarConvocatoriaResponse
)

from app.services.convocatoria_service import (
    registrar_convocatoria,
    cerrar_convocatoria,
    obtener_todas_las_convocatorias
)


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


@router.get("/", response_model=list[ConvocatoriaResumen])
def listar():
    return obtener_todas_las_convocatorias()


@router.patch(
    "/{id_convocatoria}/cerrar",
    response_model=CerrarConvocatoriaResponse
)
def cerrar(
    id_convocatoria: int,
    usuario_actual: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        resultado = cerrar_convocatoria(id_convocatoria)

        return {
            "mensaje": "Convocatoria cerrada correctamente",
            "id_convocatoria": resultado["id_convocatoria"],
            "titulo": resultado["titulo"],
            "estado": resultado["estado"]
        }

    except ValueError as error:
        detalle = str(error)

        codigo = 404 if "no existe" in detalle else 400

        raise HTTPException(status_code=codigo, detail=detalle)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al cerrar la convocatoria."
        )