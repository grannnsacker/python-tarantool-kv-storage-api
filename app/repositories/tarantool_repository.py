import asyncio
from app.repositories import ConnectionRepository


class TarantoolRepository:
    def __init__(self, connect_repository: ConnectionRepository):
        self.connect_repository = connect_repository

    async def set_keys_values(self, items: dict):
        future = []
        for k, v in items.items():
            future.append(asyncio.create_task(self._set_key_value(k, v)))

        await asyncio.gather(*future)

    async def _set_key_value(self, key, value):
        conn = await self.connect_repository.get_connection()
        return await conn.insert(space="kv_store", t=(key, value), replace=True)

    async def get_values(self, keys: list):
        future = []
        for key in keys:
            future.append(asyncio.create_task(self._get_value(key)))

        results = await asyncio.gather(*future)
        data = dict()
        for i, ans in enumerate(results):
            if len(ans) > 0:
                data[keys[i]] = ans[0][1]
            else:
                data[keys[i]] = None
        return data

    async def _get_value(self, key):
        conn = await self.connect_repository.get_connection()
        result = await conn.select(space="kv_store", key=[key])
        return result


