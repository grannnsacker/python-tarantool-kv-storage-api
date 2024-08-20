from typing import Annotated

from fastapi import APIRouter, Depends

from app.controllers.login import login_controller
from app.models.credential import UserCredential
from app.models.user import User
from app.repositories import UserRepository, get_user_repository
from app.security.utility import get_current_user

login_router = APIRouter()


@login_router.post("/login")
async def login_handler(credential: UserCredential,
                        user_repository: Annotated[UserRepository,
                                                   Depends(get_user_repository,
                                                           use_cache=True)]):
    """
    Asynchronous handler function for the "/login" route.

    :param credential: UserCredential object containing username and password.
    :param user_repository: UserRepository object responsible for interacting
                            with the database to retrieve user data.
    :return: Asynchronous controller call
    """

    return await login_controller(credential, user_repository)

