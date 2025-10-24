from datetime import timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.utils.helper import get_current_time

# Use passlib's bcrypt_sha256 scheme. Passlib will pre-hash with
# SHA-256 before calling bcrypt which avoids the bcrypt 72-byte limit.
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt_sha256"],
    deprecated="auto",
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = get_current_time() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def needs_rehash(hashed_password: str) -> bool:
    """Return True if the stored hash should be upgraded to the
    current preferred scheme/parameters.
    """
    try:
        return pwd_context.needs_update(hashed_password)
    except Exception:
        return False


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
