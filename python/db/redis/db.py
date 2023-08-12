from typing import Dict
from redis import Redis, ConnectionPool, ConnectionError
from config import settings
from dotenv import load_dotenv
import os

load_dotenv((settings.BASE_DIR / ".env").resolve(strict=True))

client = Redis(
    host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", "6379"))
)


def fetch_data():
    client.hget()
    ...


def topK_query(query: str | list[float]):
    client.topk()
    ...


def put_data(data: Dict[str, str | float | int | bytes]):
    client.hset(data)
    # ...
