"""
Configuración de fixtures para pytest
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models import Sucursal, UsuarioAdmin
from app.auth import get_password_hash

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Fixture que provee una sesión de base de datos limpia para cada test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Fixture que provee un cliente de prueba para la API"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_sucursales(db):
    """Fixture que crea sucursales de prueba"""
    sucursales = [
        Sucursal(
            nombre="Sucursal Test 1",
            ciudad="Ciudad de México",
            direccion="Av. Test 123",
            telefono="55-1234-5678"
        ),
        Sucursal(
            nombre="Sucursal Test 2",
            ciudad="Monterrey",
            direccion="Blvd. Test 456",
            telefono="81-8765-4321"
        ),
    ]
    for sucursal in sucursales:
        db.add(sucursal)
    db.commit()
    for sucursal in sucursales:
        db.refresh(sucursal)
    return sucursales


@pytest.fixture(scope="function")
def test_admin_user(db):
    """Fixture que crea un usuario admin de prueba"""
    admin = UsuarioAdmin(
        username="testadmin",
        password_hash=get_password_hash("testpass123"),
        email="testadmin@test.com"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture(scope="function")
def auth_token(client, test_admin_user):
    """Fixture que provee un token JWT válido"""
    response = client.post(
        "/api/auth/login",
        json={"username": "testadmin", "password": "testpass123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

