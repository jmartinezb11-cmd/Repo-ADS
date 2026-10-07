from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import require_role
from app.core.roles import Role
from app.schemas.documento import ValidarDocumento
from app.services.documento_service import procesar_validacion


router = APIRouter(
    prefix="/api/documentos",
    tags=["Documentos"]
)


# US-016 - Validar documentación

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
            data.comentario_validacion
        )

        return {
            "mensaje": "Documento validado correctamente",
            "documento": documento
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al validar el documento."
        )
