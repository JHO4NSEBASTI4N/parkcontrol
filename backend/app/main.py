from fastapi import FastAPI
from app.core.config import configuracion

app = FastAPI(
    title = configuracion.app_name,
    version = configuracion.app_version,
    description = "API REST para el control de parqueaderos"
)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a park control",
        "version": configuracion.app_version,
        "estado": "API Funcionando"
    }
    
@app.get("/saludo")
def verificar_saludo():
    return {
        "mensaje": "Hola, bienvenido a park control"
    }