from pydantic import BaseModel


class ValidarDocumento(BaseModel):
    estado_validacion: str  # "aprobado" o "rechazado"
    comentario_validacion: str | None = None
