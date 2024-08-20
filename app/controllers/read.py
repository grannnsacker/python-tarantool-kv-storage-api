from app.models.response import ReadResponse
from app.models.request import ReadRequest


async def read_controller(keys: ReadRequest,
                          tarantool_repository):
    """
    Asynchronous controller function for handling read requests.

    :param keys: ReadRequest object containing the keys for which data should be retrieved.
    :param tarantool_repository: TarantoolRepository instance used to interact with the Tarantool
                                 database for fetching data.

    The function calls the get_values method of the tarantool_repository to retrieve data
    corresponding to the provided keys.
    The retrieved data is then encapsulated in a ReadResponse object and returned.

    :return: A ReadResponse object containing the data retrieved from the database.
    """

    data = await tarantool_repository.get_values(keys.keys)
    response = ReadResponse(data=data)
    return response
