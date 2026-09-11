from fastapi import Depends, HTTPException, status
from app.core.roles import Role

MOCK_USERS_DB = {
    "token-estudiante": {"id": 1, "nombre": "Estudiante Demo", "rol": Role.ESTUDIANTE},
    "token-evaluador": {"id": 2, "nombre": "Evaluador Demo", "rol": Role.EVALUADOR},
    "token-admin": {"id": 3, "nombre": "Admin Demo", "rol": Role.ADMINISTRADOR},
}

def get_current_user(token: str = "token-estudiante"):
    user = MOCK_USERS_DB.get(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
        )
    return user


def require_role(*roles_permitidos: Role):
    def verificador(user: dict = Depends(get_current_user)):
        if user["rol"] not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: se requiere rol {', '.join(r.value for r in roles_permitidos)}"
            )
        return user
    return verificador
