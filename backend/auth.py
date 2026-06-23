import uuid

from fastapi import HTTPException, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

sessions = {}

security = HTTPBearer()


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_token(email):
    token = str(uuid.uuid4())

    sessions[token] = email

    return token


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    if token not in sessions:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    return sessions[token]