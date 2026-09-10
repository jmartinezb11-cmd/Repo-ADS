from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.estudiantes import router as estudiantes_router 
from app.api.routes.auth import router as auth_router


app = FastAPI(
    title="Sistema de Gestión de Becas",
    description="API del proyecto ADS",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(estudiantes_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "API del Sistema de Gestión de Becas funcionando"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }