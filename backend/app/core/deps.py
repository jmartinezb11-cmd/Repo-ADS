from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt

from app.core.roles import Role
from app.core.security import verificar_token
from app.repositories.estudiante_repository import (
    obtener_estudiante_por_id
)


esquema_token = HTTPBearer()


def get_current_user(
    credenciales: HTTPAuthorizationCredentials = Depends(esquema_token)
) -> dict:

    token = credenciales.credentials

    try:
        datos_token = verificar_token(token)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tu sesión expiró, inicia sesión de nuevo."
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido."
        )

    estudiante = obtener_estudiante_por_id(datos_token["id_estudiante"])

    if estudiante is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado."
        )

    if estudiante["estado_cuenta"] == "inactivo":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tu cuenta se encuentra inactiva."
        )

    return {
        "id": estudiante["id_estudiante"],
        "nombre": f"{estudiante['primer_nombre']} {estudiante['primer_apellido']}",
        "rol": Role(estudiante["rol"])
    }


def require_role(*roles_permitidos: Role):
    def verificador(user: dict = Depends(get_current_user)):
        if user["rol"] not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Acceso denegado: se requiere rol "
                    + ", ".join(r.value for r in roles_permitidos)
                )
            )
        return user

    return verificador