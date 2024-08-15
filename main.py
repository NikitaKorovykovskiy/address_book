from fastapi import FastAPI, HTTPException, Depends
import redis.asyncio as redis
from models import Address, MessageResponse, Settings, WriteAddress
from typing import AsyncGenerator


settings = Settings()


async def get_redis_connection() -> AsyncGenerator[redis.Redis, None]:
    redis_connection = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
    )
    try:
        yield redis_connection
    finally:
        await redis_connection.close()


app = FastAPI()


@app.post(
    "/write_data/",
    response_model=MessageResponse,
    status_code=201,
    summary="Добавить или обновить адрес",
)
async def write_or_update_address(
    data: WriteAddress,
    redis_conn: redis.Redis = Depends(get_redis_connection),
) -> MessageResponse:
    try:
        existing_address = await redis_conn.get(data.phone)

        if existing_address:
            await redis_conn.set(data.phone, data.address)
            return MessageResponse(message="Адрес успешно обновлен")
        else:
            await redis_conn.set(data.phone, data.address)
            return MessageResponse(message="Адрес успешно добавлен")
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Ошибка подключения к Redis")


@app.get("/check_data/", status_code=200, summary="Проверить адрес")
async def get_address(
    phone: str,
    redis_conn: redis.Redis = Depends(get_redis_connection),
) -> Address | dict:
    try:
        address = await redis_conn.get(phone)
        if not address:
            return {"message": "По данному номеру не зарегистрировано адреса"}
        return {"address": address}
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Ошибка подключения к Redis")
