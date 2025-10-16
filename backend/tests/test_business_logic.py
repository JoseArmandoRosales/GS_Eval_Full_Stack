"""
Pruebas unitarias para la lógica de negocio
"""
import pytest
from decimal import Decimal
from app.business_logic import evaluar_solicitud_credito, calcular_cuota_mensual


class TestEvaluacionSolicitud:
    """Tests para la evaluación de solicitudes de crédito"""
    
    def test_solicitud_aprobada_caso_ideal(self):
        """Test de solicitud aprobada con todos los parámetros ideales"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=35,
            monto_solicitado=Decimal("100000"),
            ingreso_mensual=Decimal("30000"),
            score_crediticio=750,
            tiene_tarjeta_credito=True,
            tiene_credito_automotriz=True,
            plazo_meses=36
        )
        assert aprobado is True
        assert motivo is None
    
    def test_rechazo_por_edad_menor(self):
        """Test de rechazo por edad menor a 18 años"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=17,
            monto_solicitado=Decimal("50000"),
            ingreso_mensual=Decimal("20000"),
            score_crediticio=700,
            tiene_tarjeta_credito=False,
            tiene_credito_automotriz=False,
            plazo_meses=24
        )
        assert aprobado is False
        assert "inferior al mínimo" in motivo
    
    def test_rechazo_por_edad_mayor(self):
        """Test de rechazo por edad mayor a 70 años"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=71,
            monto_solicitado=Decimal("50000"),
            ingreso_mensual=Decimal("20000"),
            score_crediticio=700,
            tiene_tarjeta_credito=True,
            tiene_credito_automotriz=False,
            plazo_meses=24
        )
        assert aprobado is False
        assert "superior al máximo" in motivo
    
    def test_rechazo_por_score_bajo(self):
        """Test de rechazo por score crediticio insuficiente"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=30,
            monto_solicitado=Decimal("50000"),
            ingreso_mensual=Decimal("20000"),
            score_crediticio=550,
            tiene_tarjeta_credito=False,
            tiene_credito_automotriz=False,
            plazo_meses=24
        )
        assert aprobado is False
        assert "Score crediticio insuficiente" in motivo
    
    def test_rechazo_por_monto_excesivo(self):
        """Test de rechazo por monto solicitado excesivo"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=30,
            monto_solicitado=Decimal("500000"),
            ingreso_mensual=Decimal("20000"),
            score_crediticio=700,
            tiene_tarjeta_credito=True,
            tiene_credito_automotriz=False,
            plazo_meses=24
        )
        assert aprobado is False
        assert "excede el máximo permitido" in motivo
    
    def test_rechazo_por_cuota_alta(self):
        """Test de rechazo por cuota mensual excesiva"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=30,
            monto_solicitado=Decimal("100000"),
            ingreso_mensual=Decimal("10000"),
            score_crediticio=700,
            tiene_tarjeta_credito=True,
            tiene_credito_automotriz=False,
            plazo_meses=12
        )
        assert aprobado is False
        assert "excede el 40%" in motivo or "excede el 35%" in motivo
    
    def test_cliente_sin_historial_rechazado(self):
        """Test de rechazo para cliente sin historial crediticio"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=25,
            monto_solicitado=Decimal("50000"),
            ingreso_mensual=Decimal("15000"),
            score_crediticio=620,
            tiene_tarjeta_credito=False,
            tiene_credito_automotriz=False,
            plazo_meses=24
        )
        assert aprobado is False
        assert "sin historial" in motivo
    
    def test_cliente_sin_historial_aprobado_con_buen_score(self):
        """Test de aprobación para cliente sin historial pero buen score"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=25,
            monto_solicitado=Decimal("30000"),
            ingreso_mensual=Decimal("20000"),
            score_crediticio=700,
            tiene_tarjeta_credito=False,
            tiene_credito_automotriz=False,
            plazo_meses=24
        )
        assert aprobado is True
        assert motivo is None
    
    def test_cliente_con_historial_score_justo(self):
        """Test para cliente con historial crediticio y score justo"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=40,
            monto_solicitado=Decimal("80000"),
            ingreso_mensual=Decimal("30000"),
            score_crediticio=620,
            tiene_tarjeta_credito=True,
            tiene_credito_automotriz=False,
            plazo_meses=36
        )
        assert aprobado is True or "35%" in motivo
    
    def test_caso_limite_edad_18(self):
        """Test caso límite: edad exactamente 18 años"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=18,
            monto_solicitado=Decimal("30000"),
            ingreso_mensual=Decimal("15000"),
            score_crediticio=680,
            tiene_tarjeta_credito=False,
            tiene_credito_automotriz=False,
            plazo_meses=24
        )
        assert aprobado is True or "sin historial" in motivo
    
    def test_caso_limite_edad_70(self):
        """Test caso límite: edad exactamente 70 años"""
        aprobado, motivo = evaluar_solicitud_credito(
            edad=70,
            monto_solicitado=Decimal("50000"),
            ingreso_mensual=Decimal("25000"),
            score_crediticio=700,
            tiene_tarjeta_credito=True,
            tiene_credito_automotriz=True,
            plazo_meses=24
        )
        assert aprobado is True
        assert motivo is None


class TestCalculoCuota:
    """Tests para el cálculo de cuota mensual"""
    
    def test_calculo_cuota_sin_interes(self):
        """Test de cálculo de cuota sin interés"""
        cuota = calcular_cuota_mensual(
            Decimal("12000"),
            12,
            Decimal("0")
        )
        assert cuota == Decimal("1000.00")
    
    def test_calculo_cuota_con_interes(self):
        """Test de cálculo de cuota con interés"""
        cuota = calcular_cuota_mensual(
            Decimal("100000"),
            36,
            Decimal("12.0")
        )
        # La cuota debe ser mayor que el capital dividido entre el plazo
        assert cuota > Decimal("2777.78")
        assert cuota < Decimal("3500.00")
    
    def test_cuota_monto_pequeno(self):
        """Test con monto pequeño"""
        cuota = calcular_cuota_mensual(
            Decimal("5000"),
            12,
            Decimal("12.0")
        )
        assert cuota > Decimal("400")
        assert cuota < Decimal("500")

