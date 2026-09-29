from pwdlib import PasswordHash

import os
from datetime import datetime, timedelta, timezone
import jwt


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave-temporal-cambiar-en-.env")
ALGORITHM = "HS256"
MINUTOS_EXPIRACION = 60


def crear_token(id_estudiante: int, rol: str) -> str:
    payload = {
        "sub": str(id_estudiante),
        "rol": rol,
        "exp": datetime.now(timezone.utc) + timedelta(
            minutes=MINUTOS_EXPIRACION
        )
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return {
        "id_estudiante": int(payload["sub"]),
        "rol": payload["rol"]
    }
