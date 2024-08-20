from concurrent.futures import ThreadPoolExecutor

from app.models.user import User
from app.repositories import ConnectionRepository


class UserRepository:
    def __init__(self, connect_repository: ConnectionRepository):
        self.connect_repository = connect_repository

    async def get(self, username: str):
        conn = await self.connect_repository.get_connection()
        result = await conn.select(space="users", key=[username])
        if result:
            user = User()
            user.username = result[0][0]
            user.password = result[0][1]
            return user
        return None

