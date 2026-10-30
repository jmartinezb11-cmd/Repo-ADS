from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Rutas del sistema
from app.api.routes.comite_routes import router as comite_router
from app.api.routes.estudiantes import router as estudiantes_router
from app.api.routes.auth import router as auth_router
from app.api.routes.usuarios import router as usuarios_router
from app.api.routes.convocatorias import router as convocatorias_router
from app.api.routes.solicitudes import router as solicitudes_router
from app.api.routes.documentos import router as documentos_router
from app.api.routes.evaluaciones import router as evaluaciones_router
from app.api.routes.reportes import router as reportes_router
from app.api.routes.decisiones import router as decisiones_router
from app.api import roles_demo
from app.api.routes.reporte_resultados import router as reporte_resultados_router

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

# Registro de routers
app.include_router(estudiantes_router)
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(convocatorias_router)
app.include_router(comite_router)
app.include_router(roles_demo.router)
app.include_router(decisiones_router)
app.include_router(solicitudes_router)
app.include_router(documentos_router)
app.include_router(evaluaciones_router)
app.include_router(reportes_router)
app.include_router(reporte_resultados_router)



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