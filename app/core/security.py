from datetime import timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import MissingBackendError, UnknownHashError

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
    """
    Verify a password against stored hash.
    - Handles UnknownHashError (e.g. when argon2 not available or hash format unknown)
    - Falls back to bcrypt_sha256 for legacy hashes
    """
    if not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (UnknownHashError, MissingBackendError):
        legacy_ctx = CryptContext(
            schemes=["bcrypt", "bcrypt_sha256"], deprecated="auto"
        )
        try:
            return legacy_ctx.verify(plain_password, hashed_password)
        except Exception:
            return False
    except Exception:
        return False


def get_password_hash(password):
    """Hash a password using the preferred context.

    If the preferred backend (e.g. argon2) is not available, fall back
    to bcrypt_sha256 so the application can still create hashes.
    """
    try:
        return pwd_context.hash(password)
    except (MissingBackendError, Exception):
        legacy_ctx = CryptContext(
            schemes=["bcrypt", "bcrypt_sha256"], deprecated="auto"
        )
        return legacy_ctx.hash(password)


def needs_rehash(hashed_password: str) -> bool:
    """Return True if the stored hash should be upgraded to the
    current preferred scheme/parameters.
    """
    try:
        return pwd_context.needs_update(hashed_password)
    except (MissingBackendError, UnknownHashError):
        return False
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
