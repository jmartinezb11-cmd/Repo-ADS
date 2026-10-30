from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import require_role
from app.core.roles import Role
from app.schemas.decision import DecisionSolicitud
from app.repositories.solicitud_repository import obtener_solicitudes_para_decision
from app.services.decision_service import (
    SolicitudNoEncontrada,
    procesar_decision,
)


router = APIRouter(
    prefix="/api/solicitudes",
    tags=["Decisiones"]
)
# US-024 - Consultar solicitudes pendientes de decisión

@router.get("/pendientes-decision")
def listar_pendientes_decision(
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        solicitudes = obtener_solicitudes_para_decision()

        return {
            "solicitudes": solicitudes
        }

    except Exception:
        import logging
        logging.getLogger(__name__).exception(
            "Error al consultar solicitudes pendientes de decisión"
        )

        raise HTTPException(
            status_code=500,
            detail="No se pudieron consultar las solicitudes pendientes."
        )

# US-024 - Aprobar o rechazar solicitud

@router.patch("/{id_solicitud}/decision")
def decidir(
    id_solicitud: int,
    data: DecisionSolicitud,
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        solicitud = procesar_decision(
            id_solicitud,
            data.decision,
            data.comentario,
            user["id"]
        )

        return {
            "mensaje": f"Solicitud {data.decision} correctamente",
            "solicitud": solicitud
        }

    except SolicitudNoEncontrada as error:
        raise HTTPException(status_code=404, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al registrar la decisión."
        )
