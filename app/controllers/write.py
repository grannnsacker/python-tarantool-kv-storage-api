from typing import Annotated
from fastapi import Depends
from app.models.request import WriteRequest
from app.repositories import get_tarantool_repository, TarantoolRepository


async def write_controller(items: WriteRequest,
                           tarantool_repository: Annotated[TarantoolRepository,
                                                           Depends(get_tarantool_repository,
                                                                   use_cache=True)]):
    """
    Asynchronous controller function for handling write requests.

    :param items: WriteRequest object containing the data to be written to the database.
    :param tarantool_repository: TarantoolRepository instance used to interact with the Tarantool
                                 database for storing data.

    The function calls the set_keys_values method of the tarantool_repository to write the provided data
    to the database.

    :return: The result of the set_keys_values method, which performs the actual write operation.
    """
    return await tarantool_repository.set_keys_values(items.data)
