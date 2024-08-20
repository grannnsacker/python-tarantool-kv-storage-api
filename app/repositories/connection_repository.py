from asyncio import exceptions

import asynctnt

from app.errors import DataBaseConnectionError


class ConnectionRepository:
    def __init__(self, host, port, username, password):
        try:
            self.conn = asynctnt.Connection(
                host=host,
                port=port,
                username=username,
                password=password,
                reconnect_timeout=0
            )
        except exceptions.TimeoutError:
            raise DataBaseConnectionError()

    async def get_connection(self) -> asynctnt.Connection:
        try:
            if not self.conn.is_connected:
                await self.conn.connect()
            return self.conn
        except exceptions.TimeoutError:
            raise DataBaseConnectionError()

    async def discard_connection(self):
        try:
            if self.conn.is_connected:
                await self.conn.disconnect()
            return self.conn
        except exceptions.TimeoutError:
            raise DataBaseConnectionError()