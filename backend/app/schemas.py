"""
Esquemas Pydantic para validación de datos
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


# ==================== Sucursales ====================
class SucursalBase(BaseModel):
    """Esquema base para sucursales"""
    nombre: str = Field(..., min_length=1, max_length=100)
    ciudad: str = Field(..., min_length=1, max_length=100)
    direccion: str = Field(..., min_length=1, max_length=255)
    telefono: Optional[str] = Field(None, max_length=20)


class SucursalCreate(SucursalBase):
    """Esquema para crear sucursales"""
    pass


class Sucursal(SucursalBase):
    """Esquema completo de sucursal"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Clientes ====================
class ClienteBase(BaseModel):
    """Esquema base para clientes"""
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: date
    edad: int = Field(..., ge=0, le=150)
    
    @validator('edad')
    def validar_edad_coherente(cls, v, values):
        """Validar que la edad sea coherente con la fecha de nacimiento"""
        if 'fecha_nacimiento' in values:
            fecha_nac = values['fecha_nacimiento']
            edad_calculada = (datetime.now().date() - fecha_nac).days // 365
            if abs(edad_calculada - v) > 1:
                raise ValueError('La edad no es coherente con la fecha de nacimiento')
        return v


class ClienteCreate(ClienteBase):
    """Esquema para crear clientes"""
    pass


class Cliente(ClienteBase):
    """Esquema completo de cliente"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Solicitudes ====================
class SolicitudBase(BaseModel):
    """Esquema base para solicitudes"""
    monto_solicitado: Decimal = Field(..., gt=0, decimal_places=2)
    ingreso_mensual: Decimal = Field(..., gt=0, decimal_places=2)
    score_crediticio: int = Field(..., ge=300, le=850)
    tiene_tarjeta_credito: bool = False
    tiene_credito_automotriz: bool = False
    plazo_meses: int = Field(..., gt=0, le=360)
    sucursal_id: int = Field(..., gt=0)


class SolicitudCreate(SolicitudBase):
    """Esquema para crear solicitud con datos del cliente"""
    # Datos del cliente
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: date
    
    @property
    def edad(self) -> int:
        """Calcular edad automáticamente desde fecha_nacimiento"""
        hoy = datetime.now().date()
        edad = hoy.year - self.fecha_nacimiento.year
        # Ajustar si aún no ha cumplido años este año
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad


class SolicitudResponse(SolicitudBase):
    """Esquema de respuesta de solicitud"""
    id: int
    cliente_id: int
    estado: str
    motivo_rechazo: Optional[str]
    fecha_solicitud: datetime
    
    # Información adicional del cliente
    cliente_nombre: Optional[str] = None
    cliente_email: Optional[str] = None
    sucursal_nombre: Optional[str] = None
    
    # Información financiera calculada
    cuota_mensual: Optional[Decimal] = None
    tasa_interes_anual: Optional[Decimal] = None
    total_a_pagar: Optional[Decimal] = None
    total_intereses: Optional[Decimal] = None
    
    class Config:
        from_attributes = True


class Solicitud(BaseModel):
    """Esquema completo de solicitud"""
    id: int
    cliente_id: int
    sucursal_id: int
    monto_solicitado: Decimal
    ingreso_mensual: Decimal
    score_crediticio: int
    tiene_tarjeta_credito: bool
    tiene_credito_automotriz: bool
    plazo_meses: int
    estado: str
    motivo_rechazo: Optional[str]
    fecha_solicitud: datetime
    
    class Config:
        from_attributes = True


# ==================== Simulación ====================
class SimulacionRequest(BaseModel):
    """Esquema para solicitar simulación de múltiples solicitudes"""
    cantidad: int = Field(..., ge=1, le=1000, description="Cantidad de solicitudes a simular")


class SimulacionResponse(BaseModel):
    """Esquema de respuesta de simulación"""
    total_generadas: int
    aprobadas: int
    rechazadas: int
    solicitudes: list[SolicitudResponse]


# ==================== Indicadores ====================
class IndicadoresPorSucursal(BaseModel):
    """Indicadores por sucursal"""
    sucursal_id: int
    sucursal_nombre: str
    ciudad: str
    total_solicitudes: int
    aprobadas: int
    rechazadas: int
    monto_promedio: Decimal
    monto_aprobado_total: Decimal


class IndicadoresGenerales(BaseModel):
    """Indicadores generales del sistema"""
    total_solicitudes: int
    total_aprobadas: int
    total_rechazadas: int
    tasa_aprobacion: float
    monto_total_solicitado: Decimal
    monto_total_aprobado: Decimal
    score_promedio: float
    por_sucursal: list[IndicadoresPorSucursal]


# ==================== Autenticación ====================
class Token(BaseModel):
    """Esquema de token JWT"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Datos contenidos en el token"""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Esquema para login"""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UsuarioAdminBase(BaseModel):
    """Esquema base para usuarios admin"""
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr


class UsuarioAdminCreate(UsuarioAdminBase):
    """Esquema para crear usuarios admin"""
    password: str = Field(..., min_length=6)


class UsuarioAdmin(UsuarioAdminBase):
    """Esquema completo de usuario admin"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

