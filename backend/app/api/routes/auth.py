from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import login_estudiante


router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación"]
)


@router.post("/login", response_model=LoginResponse, status_code=200)
def login(data: LoginRequest):

    try:
        resultado = login_estudiante(
            email=str(data.email),
            password=data.password
        )

        return {
            "mensaje": "Inicio de sesión exitoso",
            "id_estudiante": resultado["id_estudiante"],
            "nombre_completo": resultado["nombre_completo"],
            "email": resultado["email"],
            "rol": resultado["rol"]
        }

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al iniciar sesión."
        )