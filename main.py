from fastapi import FastAPI, HTTPException
import redis
import logging

from models import Address, WriteAddress
from settings import REDIS_DB, REDIS_HOST, REDIS_PORT

logger = logging.getLogger("redis")

try:
    redis_connection = redis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
    )
except redis.ConnectionError as e:
    logger.error(f"Ошибка подключения к Redis: {e}")


app = FastAPI()


@app.post("/write_data/", response_model=dict, summary="Добавить новый адрес")
def write_address(data: WriteAddress) -> dict:
    try:
        redis_connection.set(data.phone, data.address)
        return {"message": "Адрес успешно добавлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Oшибка: " + str(e))


# Хоть редис и автоматически обновляет значение по ключу, но разделил для использования put запроса
@app.put("/write_data/", response_model=dict, summary="Обновить адрес")
def update_address(data: WriteAddress) -> dict[str]:
    try:
        redis_connection.set(data.phone, data.address)
        return {"message": "Адрес успешно обновлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Oшибка: " + str(e))


@app.get("/check_data/", summary="Добавить адрес")
def get_address(phone: str) -> Address | dict:
    try:
        address = redis_connection.get(phone)
        if not address:
            return {"message": "По данному номеру не зарегистрировано адреса"}
        return {"address": address}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка" + str(e))
