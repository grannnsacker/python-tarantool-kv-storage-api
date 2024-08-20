from fastapi import Depends

from .connection_repository import ConnectionRepository
from .tarantool_repository import TarantoolRepository
from .user_repository import UserRepository
from app.conf import DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD


async def get_connection_repository():
    connection_repository = ConnectionRepository(host=DB_HOST, port=DB_PORT,
                                                 username=DB_USERNAME, password=DB_PASSWORD)
    return connection_repository


async def get_user_repository(connection_repository=Depends(get_connection_repository, use_cache=True)):
    user_repository = UserRepository(connection_repository)
    return user_repository


async def get_tarantool_repository(connection_repository=Depends(get_connection_repository, use_cache=True)):
    tarantool_repository = TarantoolRepository(connection_repository)
    return tarantool_repository





