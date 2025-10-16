"""
Operaciones CRUD para la base de datos
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
import random
from . import models, schemas
from .business_logic import evaluar_solicitud_credito, calcular_cuota_mensual


def get_sucursales(db: Session, skip: int = 0, limit: int = 100) -> List[models.Sucursal]:
    """Obtener lista de sucursales"""
    return db.query(models.Sucursal).offset(skip).limit(limit).all()


def get_sucursal(db: Session, sucursal_id: int) -> Optional[models.Sucursal]:
    """Obtener una sucursal por ID"""
    return db.query(models.Sucursal).filter(models.Sucursal.id == sucursal_id).first()


def get_cliente_por_email(db: Session, email: str) -> Optional[models.Cliente]:
    """Obtener un cliente por email"""
    return db.query(models.Cliente).filter(models.Cliente.email == email).first()


def crear_cliente(db: Session, cliente_data: dict) -> models.Cliente:
    """Crear un nuevo cliente"""
    cliente = models.Cliente(**cliente_data)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def crear_solicitud(
    db: Session,
    solicitud_data: schemas.SolicitudCreate
) -> schemas.SolicitudResponse:
    """
    Crear una nueva solicitud de crédito
    1. Crear o buscar cliente
    2. Evaluar solicitud
    3. Guardar en BD
    """
    # Verificar que la sucursal existe
    sucursal = get_sucursal(db, solicitud_data.sucursal_id)
    if not sucursal:
        raise ValueError(f"Sucursal con ID {solicitud_data.sucursal_id} no existe")
    
    # Buscar o crear cliente
    cliente = get_cliente_por_email(db, solicitud_data.email)
    if not cliente:
        cliente_data = {
            "nombre": solicitud_data.nombre,
            "apellido": solicitud_data.apellido,
            "email": solicitud_data.email,
            "telefono": solicitud_data.telefono,
            "fecha_nacimiento": solicitud_data.fecha_nacimiento,
            "edad": solicitud_data.edad
        }
        cliente = crear_cliente(db, cliente_data)
    
    # Evaluar solicitud
    aprobado, motivo_rechazo = evaluar_solicitud_credito(
        edad=solicitud_data.edad,
        monto_solicitado=solicitud_data.monto_solicitado,
        ingreso_mensual=solicitud_data.ingreso_mensual,
        score_crediticio=solicitud_data.score_crediticio,
        tiene_tarjeta_credito=solicitud_data.tiene_tarjeta_credito,
        tiene_credito_automotriz=solicitud_data.tiene_credito_automotriz,
        plazo_meses=solicitud_data.plazo_meses
    )
    
    # Crear solicitud en BD
    solicitud = models.Solicitud(
        cliente_id=cliente.id,
        sucursal_id=solicitud_data.sucursal_id,
        monto_solicitado=solicitud_data.monto_solicitado,
        ingreso_mensual=solicitud_data.ingreso_mensual,
        score_crediticio=solicitud_data.score_crediticio,
        tiene_tarjeta_credito=solicitud_data.tiene_tarjeta_credito,
        tiene_credito_automotriz=solicitud_data.tiene_credito_automotriz,
        plazo_meses=solicitud_data.plazo_meses,
        estado="aprobado" if aprobado else "rechazado",
        motivo_rechazo=motivo_rechazo
    )
    
    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)
    
    # Calcular datos financieros si es aprobado
    cuota_mensual = None
    tasa_interes_anual = None
    total_a_pagar = None
    total_intereses = None
    
    if aprobado:
        tasa_interes_anual = Decimal("12.0")  # Tasa fija del 12% anual
        cuota_mensual = calcular_cuota_mensual(
            monto=solicitud_data.monto_solicitado,
            plazo_meses=solicitud_data.plazo_meses,
            tasa_anual=tasa_interes_anual
        )
        total_a_pagar = cuota_mensual * solicitud_data.plazo_meses
        total_intereses = total_a_pagar - solicitud_data.monto_solicitado
    
    # Construir respuesta
    response = schemas.SolicitudResponse(
        id=solicitud.id,
        cliente_id=solicitud.cliente_id,
        sucursal_id=solicitud.sucursal_id,
        monto_solicitado=solicitud.monto_solicitado,
        ingreso_mensual=solicitud.ingreso_mensual,
        score_crediticio=solicitud.score_crediticio,
        tiene_tarjeta_credito=solicitud.tiene_tarjeta_credito,
        tiene_credito_automotriz=solicitud.tiene_credito_automotriz,
        plazo_meses=solicitud.plazo_meses,
        estado=solicitud.estado,
        motivo_rechazo=solicitud.motivo_rechazo,
        fecha_solicitud=solicitud.fecha_solicitud,
        cliente_nombre=f"{cliente.nombre} {cliente.apellido}",
        cliente_email=cliente.email,
        sucursal_nombre=sucursal.nombre,
        cuota_mensual=cuota_mensual,
        tasa_interes_anual=tasa_interes_anual,
        total_a_pagar=total_a_pagar,
        total_intereses=total_intereses
    )
    
    return response


def simular_solicitudes(db: Session, cantidad: int) -> schemas.SimulacionResponse:
    """
    Simular múltiples solicitudes aleatorias
    """
    sucursales = get_sucursales(db)
    if not sucursales:
        raise ValueError("No hay sucursales disponibles")
    
    nombres = ["Juan", "María", "Carlos", "Ana", "Pedro", "Laura", "Luis", "Sofia", "Jorge", "Carmen"]
    apellidos = ["García", "Rodríguez", "Martínez", "López", "Hernández", "González", "Pérez", "Sánchez", "Ramírez", "Torres"]
    
    solicitudes_creadas = []
    aprobadas = 0
    rechazadas = 0
    
    for i in range(cantidad):
        # Generar datos aleatorios
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        edad = random.randint(18, 70)
        fecha_nac = date(datetime.now().year - edad, random.randint(1, 12), random.randint(1, 28))
        
        solicitud_data = schemas.SolicitudCreate(
            # Datos del cliente
            nombre=nombre,
            apellido=apellido,
            email=f"{nombre.lower()}.{apellido.lower()}{i}@email.com",
            telefono=f"55-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            fecha_nacimiento=fecha_nac,
            edad=edad,
            # Datos de la solicitud
            monto_solicitado=Decimal(str(random.randint(5000, 500000))),
            ingreso_mensual=Decimal(str(random.randint(5000, 100000))),
            score_crediticio=random.randint(400, 800),
            tiene_tarjeta_credito=random.choice([True, False]),
            tiene_credito_automotriz=random.choice([True, False]),
            plazo_meses=random.choice([12, 24, 36, 48, 60]),
            sucursal_id=random.choice(sucursales).id
        )
        
        try:
            solicitud = crear_solicitud(db, solicitud_data)
            solicitudes_creadas.append(solicitud)
            if solicitud.estado == "aprobado":
                aprobadas += 1
            else:
                rechazadas += 1
        except Exception as e:
            print(f"Error creando solicitud {i}: {e}")
            continue
    
    return schemas.SimulacionResponse(
        total_generadas=len(solicitudes_creadas),
        aprobadas=aprobadas,
        rechazadas=rechazadas,
        solicitudes=solicitudes_creadas
    )


def get_indicadores(db: Session) -> schemas.IndicadoresGenerales:
    """
    Obtener indicadores generales y por sucursal
    """
    # Indicadores generales
    total_solicitudes = db.query(func.count(models.Solicitud.id)).scalar()
    total_aprobadas = db.query(func.count(models.Solicitud.id)).filter(
        models.Solicitud.estado == "aprobado"
    ).scalar()
    total_rechazadas = db.query(func.count(models.Solicitud.id)).filter(
        models.Solicitud.estado == "rechazado"
    ).scalar()
    
    tasa_aprobacion = (total_aprobadas / total_solicitudes * 100) if total_solicitudes > 0 else 0
    
    monto_total_solicitado_raw = db.query(func.sum(models.Solicitud.monto_solicitado)).scalar()
    monto_total_solicitado = round(monto_total_solicitado_raw, 2) if monto_total_solicitado_raw else Decimal("0.00")
    
    monto_total_aprobado_raw = db.query(func.sum(models.Solicitud.monto_solicitado)).filter(
        models.Solicitud.estado == "aprobado"
    ).scalar()
    monto_total_aprobado = round(monto_total_aprobado_raw, 2) if monto_total_aprobado_raw else Decimal("0.00")
    
    score_promedio = db.query(func.avg(models.Solicitud.score_crediticio)).scalar() or 0
    
    # Indicadores por sucursal
    indicadores_sucursal = []
    sucursales = get_sucursales(db)
    
    for sucursal in sucursales:
        total_suc = db.query(func.count(models.Solicitud.id)).filter(
            models.Solicitud.sucursal_id == sucursal.id
        ).scalar()
        
        aprobadas_suc = db.query(func.count(models.Solicitud.id)).filter(
            and_(
                models.Solicitud.sucursal_id == sucursal.id,
                models.Solicitud.estado == "aprobado"
            )
        ).scalar()
        
        rechazadas_suc = db.query(func.count(models.Solicitud.id)).filter(
            and_(
                models.Solicitud.sucursal_id == sucursal.id,
                models.Solicitud.estado == "rechazado"
            )
        ).scalar()
        
        monto_promedio_raw = db.query(func.avg(models.Solicitud.monto_solicitado)).filter(
            models.Solicitud.sucursal_id == sucursal.id
        ).scalar()
        monto_promedio = round(monto_promedio_raw, 2) if monto_promedio_raw else Decimal("0.00")
        
        monto_aprobado_total_raw = db.query(func.sum(models.Solicitud.monto_solicitado)).filter(
            and_(
                models.Solicitud.sucursal_id == sucursal.id,
                models.Solicitud.estado == "aprobado"
            )
        ).scalar()
        monto_aprobado_total = round(monto_aprobado_total_raw, 2) if monto_aprobado_total_raw else Decimal("0.00")
        
        indicadores_sucursal.append(
            schemas.IndicadoresPorSucursal(
                sucursal_id=sucursal.id,
                sucursal_nombre=sucursal.nombre,
                ciudad=sucursal.ciudad,
                total_solicitudes=total_suc,
                aprobadas=aprobadas_suc,
                rechazadas=rechazadas_suc,
                monto_promedio=monto_promedio,
                monto_aprobado_total=monto_aprobado_total
            )
        )
    
    return schemas.IndicadoresGenerales(
        total_solicitudes=total_solicitudes,
        total_aprobadas=total_aprobadas,
        total_rechazadas=total_rechazadas,
        tasa_aprobacion=round(tasa_aprobacion, 2),
        monto_total_solicitado=monto_total_solicitado,
        monto_total_aprobado=monto_total_aprobado,
        score_promedio=round(score_promedio, 2),
        por_sucursal=indicadores_sucursal
    )


def get_solicitudes_recientes(db: Session, limit: int = 50) -> List[models.Solicitud]:
    """Obtener solicitudes recientes"""
    return db.query(models.Solicitud)\
        .order_by(models.Solicitud.fecha_solicitud.desc())\
        .limit(limit)\
        .all()

