from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import require_role
from app.core.roles import Role
from app.core.convocatorias_mock import CONVOCATORIAS_DB

router = APIRouter(prefix="/convocatorias", tags=["Convocatorias"])

@router.patch("/{convocatoria_id}/publicar")
def publicar_convocatoria(
    convocatoria_id: int,
    user: dict = Depends(require_role(Role.ADMINISTRADOR))
):
    convocatoria = CONVOCATORIAS_DB.get(convocatoria_id)

    if not convocatoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Convocatoria no encontrada"
        )

    if convocatoria["estado"] != "borrador":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede publicar: la convocatoria está en estado '{convocatoria['estado']}'"
        )

    convocatoria["estado"] = "publicada"
    return {
        "mensaje": "Convocatoria publicada correctamente",
        "convocatoria": convocatoria
    }
