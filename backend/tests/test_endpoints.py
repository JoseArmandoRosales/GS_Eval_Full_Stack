"""
Pruebas unitarias para los endpoints de la API
"""
import pytest
from datetime import date


class TestHealthEndpoints:
    """Tests para endpoints de health check"""
    
    def test_root_endpoint(self, client):
        """Test del endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self, client):
        """Test del health check"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestSucursalesEndpoints:
    """Tests para endpoints de sucursales"""
    
    def test_listar_sucursales(self, client, test_sucursales):
        """Test de listado de sucursales"""
        response = client.get("/api/sucursales")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        assert data[0]["nombre"] == "Sucursal Test 1"


class TestSolicitudesEndpoints:
    """Tests para endpoints de solicitudes"""
    
    def test_crear_solicitud_exitosa(self, client, test_sucursales):
        """Test de creación exitosa de solicitud"""
        solicitud_data = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": "juan.perez@test.com",
            "telefono": "55-1234-5678",
            "fecha_nacimiento": "1990-01-15",
            "monto_solicitado": 100000,
            "ingreso_mensual": 30000,
            "score_crediticio": 720,
            "tiene_tarjeta_credito": True,
            "tiene_credito_automotriz": False,
            "plazo_meses": 36,
            "sucursal_id": test_sucursales[0].id
        }
        
        response = client.post("/api/solicitudes", json=solicitud_data)
        assert response.status_code == 201
        data = response.json()
        assert data["estado"] in ["aprobado", "rechazado"]
        assert "id" in data
        assert data["cliente_nombre"] == "Juan Pérez"
    
    def test_crear_solicitud_rechazada_edad(self, client, test_sucursales):
        """Test de solicitud rechazada por edad"""
        solicitud_data = {
            "nombre": "Pedro",
            "apellido": "López",
            "email": "pedro.lopez@test.com",
            "telefono": "55-9876-5432",
            "fecha_nacimiento": "2008-10-01",
            "monto_solicitado": 50000,
            "ingreso_mensual": 20000,
            "score_crediticio": 700,
            "tiene_tarjeta_credito": False,
            "tiene_credito_automotriz": False,
            "plazo_meses": 24,
            "sucursal_id": test_sucursales[0].id
        }
        
        response = client.post("/api/solicitudes", json=solicitud_data)
        assert response.status_code == 201
        data = response.json()
        assert data["estado"] == "rechazado"
        assert "edad" in data["motivo_rechazo"].lower()
    
    def test_crear_solicitud_sin_sucursal(self, client):
        """Test de error al crear solicitud sin sucursal válida"""
        solicitud_data = {
            "nombre": "Ana",
            "apellido": "García",
            "email": "ana.garcia@test.com",
            "telefono": "55-1111-2222",
            "fecha_nacimiento": "1985-05-20",
            "monto_solicitado": 75000,
            "ingreso_mensual": 25000,
            "score_crediticio": 680,
            "tiene_tarjeta_credito": True,
            "tiene_credito_automotriz": False,
            "plazo_meses": 36,
            "sucursal_id": 9999
        }
        
        response = client.post("/api/solicitudes", json=solicitud_data)
        assert response.status_code == 400
    
    def test_solicitud_datos_invalidos(self, client, test_sucursales):
        """Test con datos inválidos"""
        solicitud_data = {
            "nombre": "María",
            "apellido": "Rodríguez",
            "email": "email-invalido",  # Email inválido
            "fecha_nacimiento": "1990-01-01",
            # edad se calcula automáticamente
            "monto_solicitado": -1000,  # Monto negativo
            "ingreso_mensual": 20000,
            "score_crediticio": 900,  # Score fuera de rango
            "tiene_tarjeta_credito": False,
            "tiene_credito_automotriz": False,
            "plazo_meses": 24,
            "sucursal_id": test_sucursales[0].id
        }
        
        response = client.post("/api/solicitudes", json=solicitud_data)
        assert response.status_code == 422  # Validation error
    
    def test_simular_solicitudes(self, client, test_sucursales):
        """Test de simulación de múltiples solicitudes"""
        response = client.post(
            "/api/solicitudes/simular",
            json={"cantidad": 5}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_generadas"] == 5
        assert data["aprobadas"] + data["rechazadas"] == 5
        assert len(data["solicitudes"]) == 5


class TestAuthEndpoints:
    """Tests para endpoints de autenticación"""
    
    def test_login_exitoso(self, client, test_admin_user):
        """Test de login exitoso"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testadmin", "password": "testpass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_credenciales_invalidas(self, client, test_admin_user):
        """Test de login con credenciales inválidas"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testadmin", "password": "wrongpassword"}
        )
        assert response.status_code == 401
    
    def test_login_usuario_inexistente(self, client):
        """Test de login con usuario inexistente"""
        response = client.post(
            "/api/auth/login",
            json={"username": "noexiste", "password": "password123"}
        )
        assert response.status_code == 401
    
    def test_obtener_usuario_actual(self, client, auth_token):
        """Test de obtención de usuario actual con token válido"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testadmin"
    
    def test_obtener_usuario_sin_token(self, client):
        """Test de obtención de usuario sin token"""
        response = client.get("/api/auth/me")
        assert response.status_code == 403


class TestIndicadoresEndpoints:
    """Tests para endpoints de indicadores"""
    
    def test_obtener_indicadores_con_auth(self, client, test_sucursales, auth_token):
        """Test de obtención de indicadores con autenticación"""
        # Primero crear algunas solicitudes
        solicitud_data = {
            "nombre": "Test",
            "apellido": "Usuario",
            "email": "test@test.com",
            "telefono": "55-1234-5678",
            "fecha_nacimiento": "1990-01-01",
            "monto_solicitado": 100000,
            "ingreso_mensual": 30000,
            "score_crediticio": 720,
            "tiene_tarjeta_credito": True,
            "tiene_credito_automotriz": False,
            "plazo_meses": 36,
            "sucursal_id": test_sucursales[0].id
        }
        client.post("/api/solicitudes", json=solicitud_data)
        
        # Obtener indicadores
        response = client.get(
            "/api/indicadores",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_solicitudes" in data
        assert "total_aprobadas" in data
        assert "total_rechazadas" in data
        assert "tasa_aprobacion" in data
        assert "por_sucursal" in data
        assert isinstance(data["por_sucursal"], list)
    
    def test_obtener_indicadores_sin_auth(self, client):
        """Test de obtención de indicadores sin autenticación"""
        response = client.get("/api/indicadores")
        assert response.status_code == 403

