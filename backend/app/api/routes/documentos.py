from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.core.deps import require_role
from app.core.roles import Role
from app.schemas.documento import DocumentoRespuesta
from app.services.documento_service import (
    cargar_documento,
    obtener_documentos_de_solicitud,
)


router = APIRouter(
    prefix="/api/documentos",
    tags=["Documentos"]
)


# US-014 - Cargar documentación

@router.post(
    "/solicitud/{id_solicitud}",
    response_model=DocumentoRespuesta,
    status_code=201
)
async def cargar(
    id_solicitud: int,
    archivo: UploadFile = File(...),
    user: dict = Depends(require_role(Role.ESTUDIANTE))
):
    try:
        contenido = await archivo.read()

        documento = cargar_documento(
            id_solicitud=id_solicitud,
            id_estudiante=user["id"],
            nombre_archivo=archivo.filename,
            contenido=contenido
        )

        return documento

    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al cargar el documento."
        )


# US-015 - Consultar documentos

@router.get(
    "/solicitud/{id_solicitud}",
    response_model=list[DocumentoRespuesta]
)
def consultar(
    id_solicitud: int,
    user: dict = Depends(require_role(Role.ESTUDIANTE))
):
    try:
        return obtener_documentos_de_solicitud(
            id_solicitud=id_solicitud,
            id_estudiante=user["id"]
        )

    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar los documentos."
        )