"""
Autenticación y manejo de JWT
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
from .models import UsuarioAdmin
from .schemas import TokenData

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generar hash de contraseña"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crear token JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """
    Decodificar y validar token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception


def authenticate_user(db: Session, username: str, password: str) -> Optional[UsuarioAdmin]:
    """
    Autenticar usuario
    """
    user = db.query(UsuarioAdmin).filter(UsuarioAdmin.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UsuarioAdmin:
    """
    Obtener usuario actual desde el token JWT
    Dependency para proteger rutas
    """
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    user = db.query(UsuarioAdmin).filter(UsuarioAdmin.username == token_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_admin_user(db: Session) -> UsuarioAdmin:
    """
    Crear usuario admin por defecto si no existe
    """
    existing_user = db.query(UsuarioAdmin).filter(
        UsuarioAdmin.username == settings.ADMIN_USERNAME
    ).first()
    
    if existing_user:
        return existing_user
    
    hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
    admin_user = UsuarioAdmin(
        username=settings.ADMIN_USERNAME,
        password_hash=hashed_password,
        email=settings.ADMIN_EMAIL
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    return admin_user

