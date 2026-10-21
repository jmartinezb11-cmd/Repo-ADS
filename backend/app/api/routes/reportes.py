from fastapi import APIRouter, Depends, HTTPException, Response

from app.core.deps import require_role
from app.core.roles import Role
from app.services.reporte_service import (
    generar_reporte_solicitudes,
    generar_pdf_solicitudes,
)


router = APIRouter(
    prefix="/api/reportes",
    tags=["Reportes"]
)


# US-026 - Generar reporte de solicitudes

@router.get("/solicitudes")
def reporte_solicitudes(
    id_convocatoria: int | None = None,
    estado: str | None = None,
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        return generar_reporte_solicitudes(id_convocatoria, estado)

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al generar el reporte."
        )


@router.get("/solicitudes/pdf")
def reporte_solicitudes_pdf(
    id_convocatoria: int | None = None,
    estado: str | None = None,
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        reporte = generar_reporte_solicitudes(id_convocatoria, estado)
        contenido = generar_pdf_solicitudes(reporte)

        return Response(
            content=contenido,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                    'attachment; filename="reporte_solicitudes.pdf"'
            }
        )

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al generar el reporte."
        )
