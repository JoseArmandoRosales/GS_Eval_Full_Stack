"""
Pruebas unitarias para autenticación
"""
import pytest
from app.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
)
from jose import JWTError


class TestPasswordHashing:
    """Tests para hashing de contraseñas"""
    
    def test_hash_password(self):
        """Test de generación de hash de contraseña"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 20
    
    def test_verify_correct_password(self):
        """Test de verificación de contraseña correcta"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_incorrect_password(self):
        """Test de verificación de contraseña incorrecta"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False
    
    def test_different_hashes_same_password(self):
        """Test que el mismo password genera diferentes hashes"""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
