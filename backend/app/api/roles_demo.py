from fastapi import APIRouter, Depends
from app.core.deps import require_role, get_current_user
from app.core.roles import Role

router = APIRouter(prefix="/roles-demo", tags=["Control de acceso"])

@router.get("/publico")
def ruta_publica():
    return {"mensaje": "Cualquiera puede ver esto"}

@router.get("/estudiante")
def ruta_estudiante(user: dict = Depends(require_role(Role.ESTUDIANTE))):
    return {"mensaje": f"Hola {user['nombre']}, acceso de estudiante concedido"}

@router.get("/admin")
def ruta_admin(user: dict = Depends(require_role(Role.ADMINISTRADOR))):
    return {"mensaje": f"Hola {user['nombre']}, acceso de administrador concedido"}