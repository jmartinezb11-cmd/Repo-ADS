
from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import require_role
from app.core.roles import Role
from app.services.reporte_resultados_service import (
    generar_reporte_resultados
)


router = APIRouter(
    prefix="/api/reportes",
    tags=["Reportes de resultados"]
)


@router.get("/resultados")
def obtener_reporte_resultados(
    id_convocatoria: int | None = None,
    estado: str | None = None,
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    try:
        return generar_reporte_resultados(
            id_convocatoria,
            estado
        )

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al generar el reporte de resultados."
        )
