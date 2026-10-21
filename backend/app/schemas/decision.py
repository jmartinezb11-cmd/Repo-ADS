from typing import Literal

from pydantic import BaseModel


class DecisionSolicitud(BaseModel):
    decision: Literal["aprobada", "rechazada"]
    comentario: str | None = None
