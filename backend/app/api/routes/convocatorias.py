from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import require_role
from app.core.roles import Role
from app.models.convocatoria import Convocatoria
from app.schemas.convocatoria import (
    ConvocatoriaCrear,
    ConvocatoriaEditar,
)
from app.services.convocatoria_service import (
    registrar_convocatoria,
    listar_convocatorias,
    buscar_convocatoria,
    editar_convocatoria,
    cambiar_estado_a_publicada,
)


router = APIRouter(
    prefix="/api/convocatorias",
    tags=["Convocatorias"]
)



# US-005 - Crear convocatoria

@router.post("/", status_code=201)
def crear(
    data: ConvocatoriaCrear,
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
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



# US-008 - Consultar convocatorias

@router.get("/")
def consultar_convocatorias():
    try:
        return listar_convocatorias()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar las convocatorias."
        )


@router.get("/{id_convocatoria}")
def consultar_convocatoria(id_convocatoria: int):
    try:
        return buscar_convocatoria(id_convocatoria)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar la convocatoria."
        )



# US-006 - Editar convocatoria

@router.put("/{id_convocatoria}")
def actualizar(
    id_convocatoria: int,
    data: ConvocatoriaEditar,
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        convocatoria = editar_convocatoria(
            id_convocatoria,
            data.model_dump()
        )

        return {
            "mensaje": "Convocatoria actualizada correctamente",
            "convocatoria": convocatoria
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al actualizar la convocatoria."
        )



# US-007 - Publicar convocatoria

@router.patch("/{id_convocatoria}/publicar")
def publicar(
    id_convocatoria: int,
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        convocatoria = cambiar_estado_a_publicada(
            id_convocatoria
        )

        return {
            "mensaje": "Convocatoria publicada correctamente",
            "convocatoria": convocatoria
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al publicar la convocatoria."
        )