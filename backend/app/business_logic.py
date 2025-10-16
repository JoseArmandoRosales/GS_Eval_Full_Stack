"""
Lógica de negocio para aprobación de créditos
"""
from decimal import Decimal
from typing import Tuple


def evaluar_solicitud_credito(
    edad: int,
    monto_solicitado: Decimal,
    ingreso_mensual: Decimal,
    score_crediticio: int,
    tiene_tarjeta_credito: bool,
    tiene_credito_automotriz: bool,
    plazo_meses: int
) -> Tuple[bool, str]:
    """
    Evaluar una solicitud de crédito según las reglas de negocio
    
    Reglas:
    1. Edad: entre 18 y 70 años
    2. Relación deuda/ingreso: cuota mensual no debe exceder 40% del ingreso
    3. Score crediticio mínimo: 600
    4. Si tiene tarjeta o crédito automotriz y score > 650: mejor evaluación
    5. Monto máximo: hasta 10x el ingreso mensual
    
    Args:
        edad: Edad del solicitante
        monto_solicitado: Monto del crédito solicitado
        ingreso_mensual: Ingreso mensual del solicitante
        score_crediticio: Score crediticio (300-850)
        tiene_tarjeta_credito: Si tiene tarjeta de crédito
        tiene_credito_automotriz: Si tiene crédito automotriz
        plazo_meses: Plazo en meses
    
    Returns:
        Tuple[bool, str]: (aprobado, motivo_rechazo)
    """
    
    # Regla 1: Validar edad
    if edad < 18:
        return False, "Edad inferior al mínimo requerido (18 años)"
    if edad > 70:
        return False, "Edad superior al máximo permitido (70 años)"
    
    # Regla 2: Score crediticio mínimo
    if score_crediticio < 600:
        return False, f"Score crediticio insuficiente"
    
    # Regla 3: Monto máximo según ingreso
    monto_maximo = ingreso_mensual * 10
    if monto_solicitado > monto_maximo:
        return False, f"Monto solicitado excede el máximo permitido (10x ingreso mensual: ${monto_maximo:,.2f})"
    
    # Regla 4: Relación deuda/ingreso (cuota mensual vs ingreso)
    # Calculamos una cuota mensual simplificada (sin intereses para simplicidad)
    cuota_mensual = monto_solicitado / plazo_meses
    porcentaje_ingreso = (cuota_mensual / ingreso_mensual) * 100
    
    if porcentaje_ingreso > 40:
        return False, f"Cuota mensual excede el 40% del ingreso ({porcentaje_ingreso:.1f}%). Considere un plazo mayor o menor monto."
    
    # Regla 5: Evaluación mejorada con historial crediticio
    # Si tiene productos crediticios y buen score, más probabilidad de aprobación
    if tiene_tarjeta_credito or tiene_credito_automotriz:
        if score_crediticio >= 650:
            # Cliente con historial positivo
            return True, None
        elif score_crediticio >= 600:
            # Cliente con historial pero score justo
            # Aplicamos criterio más estricto en relación deuda/ingreso
            if porcentaje_ingreso > 35:
                return False, f"Para su perfil crediticio, la cuota mensual no debe exceder el 35% del ingreso ({porcentaje_ingreso:.1f}%)"
            return True, None
    
    # Cliente sin historial crediticio (primera vez)
    if not tiene_tarjeta_credito and not tiene_credito_automotriz:
        # Criterios más estrictos para clientes nuevos
        if score_crediticio < 650:
            return False, "Para clientes sin historial crediticio se requiere score mínimo de 650"
        if porcentaje_ingreso > 30:
            return False, f"Para clientes sin historial crediticio, la cuota no debe exceder el 30% del ingreso ({porcentaje_ingreso:.1f}%)"
        # Límite más bajo para clientes nuevos
        if monto_solicitado > ingreso_mensual * 5:
            return False, "Para clientes sin historial crediticio, el monto máximo es 5x el ingreso mensual"
    
    # Si pasa todas las validaciones
    return True, None


def calcular_cuota_mensual(monto: Decimal, plazo_meses: int, tasa_anual: Decimal = Decimal("12.0")) -> Decimal:
    """
    Calcular cuota mensual con intereses (fórmula simplificada)
    
    Args:
        monto: Monto del crédito
        plazo_meses: Plazo en meses
        tasa_anual: Tasa de interés anual (por defecto 12%)
    
    Returns:
        Cuota mensual
    """
    tasa_mensual = tasa_anual / 12 / 100
    
    if tasa_mensual == 0:
        return monto / plazo_meses
    
    # Fórmula de cuota fija
    cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** plazo_meses) / \
            ((1 + tasa_mensual) ** plazo_meses - 1)
    
    return cuota.quantize(Decimal("0.01"))


def obtener_recomendaciones(
    monto_solicitado: Decimal,
    ingreso_mensual: Decimal,
    plazo_meses: int,
    score_crediticio: int
) -> dict:
    """
    Obtener recomendaciones para mejorar la solicitud
    
    Returns:
        dict con recomendaciones
    """
    recomendaciones = []
    
    cuota = monto_solicitado / plazo_meses
    porcentaje = (cuota / ingreso_mensual) * 100
    
    if porcentaje > 40:
        plazo_recomendado = int((monto_solicitado / (ingreso_mensual * Decimal("0.35"))).to_integral_value())
        recomendaciones.append(f"Considere extender el plazo a {plazo_recomendado} meses")
        
        monto_recomendado = ingreso_mensual * Decimal("0.35") * plazo_meses
        recomendaciones.append(f"O reduzca el monto a ${monto_recomendado:,.2f}")
    
    if score_crediticio < 650:
        recomendaciones.append("Mejore su score crediticio para mejores condiciones")
    
    return {
        "cuota_mensual_estimada": float(cuota),
        "porcentaje_ingreso": float(porcentaje),
        "recomendaciones": recomendaciones
    }

