import asyncio
from typing import Optional

import redis.asyncio as redis


class RedisRepository:
    def __init__(self, redis_url: str):
        self._redis = redis.from_url(redis_url)

    async def set_user(self, user_id: int, full_name: str) -> None:
        key = f"user:{user_id}"
        await self._redis.set(key, full_name)

    async def get_user(self, user_id: int) -> Optional[str]:
        key = f"user:{user_id}"
        value = await self._redis.get(key)
        if value is None:
            return None
        return value.decode('utf-8')

    async def delete_user(self, user_id: int) -> None:
        key = f"user:{user_id}"
        await self._redis.delete(key)

    async def close(self):
        await self._redis.close()


#testing
async def main():
    repo = RedisRepository("redis://localhost:6379")
    await repo.set_user(1, "stepan karpov")
    name = await repo.get_user(1)
    print(f"1: {name}")
    await repo.delete_user(1)
    name_after_delete = await repo.get_user(1)
    print(f"deleted: {name_after_delete}")
    await repo.close()


if __name__ == "__main__":
    asyncio.run(main())
    