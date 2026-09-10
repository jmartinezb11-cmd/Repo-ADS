from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Gestión de Becas",
    description="API del proyecto ADS",
    version="1.0.0"
)


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


from app.api import roles_demo
app.include_router(roles_demo.router)