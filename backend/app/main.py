from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from app.core.config import configuracion
from app.api.v1.endpoints.auth import router as router_autenticacion
from app.api.v1.endpoints.dashboard import router as router_dashboard
from app.api.v1.endpoints.vehiculos import router as router_vehiculos
from app.api.v1.endpoints import clientes
from app.api.v1.endpoints import movimientos
from app.api.v1.endpoints import tarifas
from app.api.v1.endpoints import pagos
from app.api.v1.endpoints import usuarios
 
app = FastAPI(
    title=configuracion.app_name,
    version=configuracion.app_version,
    description="API REST para el control de parqueaderos"
)
 
# CORS: permitir la comunicación con el frontend de Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# Rutas de autenticación
app.include_router(router_autenticacion)
 
# Rutas del dashboard
app.include_router(router_dashboard)
 
# Ruta del Vehiculo
app.include_router(router_vehiculos)
 
# Ruta del Cliente
app.include_router(clientes.router)
 
# Ruta del Movimiento
app.include_router(movimientos.router)
 
# Ruta de las Tarifas
app.include_router(tarifas.router)
 
# Ruta de Pagos
app.include_router(pagos.router)
 
# Ruta de Usuarios
app.include_router(usuarios.router)
 
 
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a ParkControl",
        "version": configuracion.app_version,
        "estado": "API Funcionando"
    }
 
 
@app.get("/saludo")
def verificar_saludo():
    return {
        "mensaje": "Hola, bienvenido a ParkControl",
        "estado": "correcto",
        "proyecto": "ParkControl"
    }
 