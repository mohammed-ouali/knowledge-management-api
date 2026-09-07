import jwt

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.core.config import settings
from app.core.exceptions import TokenExpiredException, InvalidTokenException

from datetime import datetime, timezone, timedelta


password_hash = PasswordHash((Argon2Hasher(),))

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(subject: str, expire_delta: timedelta | None = None) -> str:
    now = datetime.now(timezone.utc)

    if expire_delta:
        expire = now + expire_delta
    else:
        expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(subject),
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(
        payload=payload,
        key=settings.secret_key,
        algorithm=settings.algorithm
    )

def create_refresh_token(subject: str, expire_delta: timedelta | None = None) -> str:
    now = datetime.now(timezone.utc)

    if expire_delta:
        expire = now + expire_delta
    else:
        expire = now + timedelta(days=settings.refresh_token_expire_days)

    payload = {
        "sub": str(subject),
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(
        payload=payload,
        key=settings.secret_key,
        algorithm=settings.algorithm
    )

def decode_token(token: str, expected_type: str = "access") -> dict:
    try:
        payload = jwt.decode(jwt=token, algorithms=[settings.algorithm], key=settings.secret_key)

    except jwt.ExpiredSignatureError:
        raise TokenExpiredException("Token has expired")
    except jwt.PyJWTError:
        raise InvalidTokenException("Invalid token signature or structure")

    token_type = payload.get("type")
    if token_type != expected_type:
        raise InvalidTokenException(
            f"Invalid token type. Expected '{expected_type}', got '{token_type}'"
        )

    return payload
