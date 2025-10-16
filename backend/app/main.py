"""
Aplicación principal FastAPI
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from . import models, schemas, crud, auth
from .database import engine, get_db
from .config import settings

# Crear tablas
models.Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Solicitud de Crédito",
    description="API para gestión de solicitudes de crédito",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Inicialización al arrancar la aplicación"""
    db = next(get_db())
    try:
        # Crear usuario admin por defecto
        auth.create_admin_user(db)
        print("✅ Usuario admin creado/verificado")
    except Exception as e:
        print(f"❌ Error al crear admin: {e}")
    finally:
        db.close()


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "API de Sistema de Solicitud de Crédito",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check"""
    return {"status": "healthy"}


# ==================== Autenticación ====================

@app.post("/api/auth/login", response_model=schemas.Token, tags=["Autenticación"])
async def login(
    login_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login para usuarios admin
    """
    user = auth.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=schemas.UsuarioAdmin, tags=["Autenticación"])
async def get_current_user_info(
    current_user: models.UsuarioAdmin = Depends(auth.get_current_user)
):
    """
    Obtener información del usuario actual
    """
    return current_user


# ==================== Sucursales ====================

@app.get("/api/sucursales", response_model=List[schemas.Sucursal], tags=["Sucursales"])
async def listar_sucursales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Listar todas las sucursales disponibles
    """
    sucursales = crud.get_sucursales(db, skip=skip, limit=limit)
    return sucursales


# ==================== Solicitudes ====================

@app.post("/api/solicitudes", response_model=schemas.SolicitudResponse, tags=["Solicitudes"], status_code=status.HTTP_201_CREATED)
async def crear_solicitud(
    solicitud: schemas.SolicitudCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva solicitud de crédito
    
    Evalúa automáticamente la solicitud y retorna el resultado (aprobado/rechazado)
    """
    try:
        resultado = crud.crear_solicitud(db, solicitud)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/api/solicitudes/simular", response_model=schemas.SimulacionResponse, tags=["Solicitudes"])
async def simular_solicitudes(
    simulacion: schemas.SimulacionRequest,
    db: Session = Depends(get_db)
):
    """
    Simular múltiples solicitudes de crédito aleatorias
    
    Útil para pruebas y generación de datos
    """
    try:
        resultado = crud.simular_solicitudes(db, simulacion.cantidad)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/solicitudes/recientes", response_model=List[schemas.Solicitud], tags=["Solicitudes"])
async def solicitudes_recientes(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.UsuarioAdmin = Depends(auth.get_current_user)
):
    """
    Obtener solicitudes recientes (requiere autenticación admin)
    """
    solicitudes = crud.get_solicitudes_recientes(db, limit=limit)
    return solicitudes


# ==================== Indicadores ====================

@app.get("/api/indicadores", response_model=schemas.IndicadoresGenerales, tags=["Indicadores"])
async def obtener_indicadores(
    db: Session = Depends(get_db),
    current_user: models.UsuarioAdmin = Depends(auth.get_current_user)
):
    """
    Obtener indicadores generales y por sucursal (requiere autenticación admin)
    
    Incluye:
    - Total de solicitudes, aprobadas y rechazadas
    - Tasa de aprobación
    - Montos totales
    - Score promedio
    - Desglose por sucursal
    """
    try:
        indicadores = crud.get_indicadores(db)
        return indicadores
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ==================== Manejo de errores ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejador personalizado de excepciones HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "detail": exc.detail,
            "status_code": exc.status_code
        },
        headers=exc.headers
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

