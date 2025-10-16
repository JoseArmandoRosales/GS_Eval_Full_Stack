"""
Modelos de base de datos con SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, DateTime, Date, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Sucursal(Base):
    """Modelo para sucursales"""
    __tablename__ = "sucursales"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    telefono = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    solicitudes = relationship("Solicitud", back_populates="sucursal")


class Cliente(Base):
    """Modelo para clientes"""
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(20))
    fecha_nacimiento = Column(Date, nullable=False)
    edad = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    solicitudes = relationship("Solicitud", back_populates="cliente")
    
    __table_args__ = (
        CheckConstraint('edad >= 0 AND edad <= 150', name='chk_edad'),
    )


class Solicitud(Base):
    """Modelo para solicitudes de crédito"""
    __tablename__ = "solicitudes"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id", ondelete="RESTRICT"), nullable=False)
    monto_solicitado = Column(DECIMAL(15, 2), nullable=False)
    ingreso_mensual = Column(DECIMAL(15, 2), nullable=False)
    score_crediticio = Column(Integer, nullable=False)
    tiene_tarjeta_credito = Column(Boolean, default=False)
    tiene_credito_automotriz = Column(Boolean, default=False)
    plazo_meses = Column(Integer, nullable=False)
    estado = Column(String(20), nullable=False)  # 'aprobado' o 'rechazado'
    motivo_rechazo = Column(Text)
    fecha_solicitud = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="solicitudes")
    sucursal = relationship("Sucursal", back_populates="solicitudes")
    
    __table_args__ = (
        CheckConstraint("estado IN ('aprobado', 'rechazado')", name='chk_estado'),
        CheckConstraint('monto_solicitado > 0', name='chk_monto_positivo'),
        CheckConstraint('ingreso_mensual > 0', name='chk_ingreso_positivo'),
        CheckConstraint('score_crediticio >= 300 AND score_crediticio <= 850', name='chk_score_range'),
        CheckConstraint('plazo_meses > 0 AND plazo_meses <= 360', name='chk_plazo_positivo'),
    )


class UsuarioAdmin(Base):
    """Modelo para usuarios administradores"""
    __tablename__ = "usuarios_admin"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

