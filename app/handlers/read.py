from typing import Annotated

from fastapi import APIRouter, Depends

from app.controllers.read import read_controller
from app.models.request import ReadRequest
from app.models.user import User
from app.repositories import TarantoolRepository, get_tarantool_repository
from app.security.utility import get_current_user

read_router = APIRouter()


@read_router.post("/read")
async def read_handler(keys: ReadRequest, current_user: Annotated[User, Depends(get_current_user)],
                       tarantool_repository: Annotated[TarantoolRepository,
                                                       Depends(get_tarantool_repository, use_cache=True)]):
    """
    Asynchronous handler function for the "/read" route.

    :param keys: ReadRequest object containing the keys for the data to be read.
    :param current_user: User object representing the currently authenticated user.
                         Obtained using the get_current_user dependency.
    :param tarantool_repository: TarantoolRepository instance responsible for
                                 interacting with the Tarantool database.
    :return: Asynchronous call to the read_controller function with keys and tarantool_repository.
    """

    return await read_controller(keys, tarantool_repository)
