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

# US-016 - Validar documentación
from fastapi.responses import FileResponse

from app.schemas.documento import ValidarDocumento, DocumentoRevisionRespuesta
from app.services.documento_service import (
    RecursoNoEncontrado,
    procesar_validacion,
    listar_para_revision,
    obtener_ruta_archivo,
)


@router.get(
    "/revision/solicitud/{id_solicitud}",
    response_model=list[DocumentoRevisionRespuesta]
)
def revisar(
    id_solicitud: int,
    user: dict = Depends(require_role(Role.EVALUADOR, Role.ADMINISTRADOR))
):
    try:
        return listar_para_revision(id_solicitud)

    except RecursoNoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al consultar los documentos."
        )


@router.get("/{id_documento}/archivo")
def descargar(
    id_documento: int,
    user: dict = Depends(require_role(Role.EVALUADOR, Role.ADMINISTRADOR))
):
    try:
        ruta, nombre = obtener_ruta_archivo(id_documento)
        return FileResponse(ruta, media_type="application/pdf", filename=nombre)

    except RecursoNoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al abrir el documento."
        )


@router.patch("/{id_documento}/validar")
def validar(
    id_documento: int,
    data: ValidarDocumento,
    user: dict = Depends(require_role(Role.EVALUADOR, Role.ADMINISTRADOR))
):
    try:
        documento = procesar_validacion(
            id_documento,
            data.estado_validacion,
            data.comentario_validacion,
            user["id"]
        )

        return {
            "mensaje": "Documento validado correctamente",
            "documento": documento
        }

    except RecursoNoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al validar el documento."
        )
