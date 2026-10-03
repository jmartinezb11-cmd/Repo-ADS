from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import require_role
from app.core.roles import Role
from app.models.convocatoria import Convocatoria
from app.schemas.convocatoria import (
    ConvocatoriaCrear,
    ConvocatoriaResumen,
    CerrarConvocatoriaResponse,
    ConvocatoriaEditar,
)
from app.services.convocatoria_service import (
    registrar_convocatoria,
    listar_convocatorias,
    buscar_convocatoria,
    editar_convocatoria,
    cambiar_estado_a_publicada,
    cerrar_convocatoria,
    obtener_todas_las_convocatorias,
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

@router.get("/", response_model=list[ConvocatoriaResumen])
def listar():
    try:
        return obtener_todas_las_convocatorias()

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


# US-009 - Cerrar convocatoria

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