from datetime import datetime, timezone, timedelta
from typing import Union, Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from .conf import SECRET_KEY, ALGORITHM
from app.repositories import UserRepository, get_user_repository
from app.models.token import TokenData
from ..errors import IncorrectUserDataException, InvalidAuthorizationTokenError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(repository: UserRepository, username: str):
    return await repository.get(username)


async def authenticate_user(repository: UserRepository, username: str, password: str):
    user = await get_user(repository, username)
    if not user or not verify_password(password, user.password):
        raise IncorrectUserDataException()
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        repository: Annotated[UserRepository, Depends(get_user_repository, use_cache=True)],
        authorization=Depends(security)
):
    token = authorization.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        expire = datetime.fromtimestamp(int(payload.get("exp")))
        if datetime.now() > expire or username is None:
            raise InvalidAuthorizationTokenError()
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise InvalidAuthorizationTokenError()
    user = await get_user(repository, username=token_data.username)
    if user is None:
        raise IncorrectUserDataException()
    return user
