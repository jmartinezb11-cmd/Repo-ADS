from pydantic import BaseModel, Field


class UsuarioResumen(BaseModel):
    id_estudiante: int
    nombre_completo: str
    email: str
    rol: str
    estado_cuenta: str


class ListaUsuariosResponse(BaseModel):
    usuarios: list[UsuarioResumen]


class CambiarEstadoRequest(BaseModel):
    nuevo_estado: str = Field(
        pattern="^(activo|inactivo|pendiente_verificacion)$"
    )


class CambiarEstadoResponse(BaseModel):
    mensaje: str
    id_estudiante: int
    nuevo_estado: str

from typing import Literal


class CambiarRolRequest(BaseModel):
    nuevo_rol: Literal["estudiante", "evaluador"]


class CambiarRolResponse(BaseModel):
    mensaje: str
    id_estudiante: int
    nuevo_rol: str