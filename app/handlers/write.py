from fastapi import APIRouter, Depends
from typing import Annotated

from app.models.response import WriteResponse, SUCCESS_WRITE_RESPONSE
from app.models.request import WriteRequest
from app.repositories import get_tarantool_repository, TarantoolRepository
from app.models.user import User
from app.security.utility import get_current_user

write_router = APIRouter()


@write_router.post("/write")
async def write_handler(items: WriteRequest,
                        current_user: Annotated[User, Depends(get_current_user)],
                        tarantool_repository: Annotated[TarantoolRepository,
                                                        Depends(get_tarantool_repository,
                                                                use_cache=True)]):
    """
    Asynchronous handler function for the "/write" route.

    :param items: WriteRequest object containing data to be written to the database.
    :param current_user: User object representing the currently authenticated user.
                       Obtained using the get_current_user dependency.
    :param tarantool_repository: TarantoolRepository instance responsible for
                               interacting with the Tarantool database.

    :return: SUCCESS_WRITE_RESPONSE indicating that the write operation was successful.
    """

    data = await tarantool_repository.set_keys_values(items.data)
    return SUCCESS_WRITE_RESPONSE
