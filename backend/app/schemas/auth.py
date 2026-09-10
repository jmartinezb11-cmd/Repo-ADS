

from pydantic import BaseModel, EmailStr, Field
 
 
class LoginRequest(BaseModel):
    email: EmailStr
 
    password: str = Field(
        min_length=1,
        max_length=128
    )
 
 
class LoginResponse(BaseModel):
    mensaje: str
    id_estudiante: int
    nombre_completo: str
    email: str
    rol: str
 
