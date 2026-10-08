from fastapi import APIRouter
from app.schemas.comite_schema import ComiteResponse
from app.services.comite_service import obtener_integrantes_comite_mock

router = APIRouter(prefix="/comite", tags=["US-023 - Comité"])

@router.get("/{id_comite}", response_model=ComiteResponse)
def consultar_comite(id_comite: int):
    """
    US-023: Consultar integrantes de un comité y sus asignaciones.
    (Funcionando con datos MOCK)
    """
    return obtener_integrantes_comite_mock(id_comite)