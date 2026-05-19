import json
import hashlib
from functools import wraps
from typing import Callable
from bson import json_util

from redis.asyncio import Redis
from dotenv import load_dotenv
from os import getenv
load_dotenv() 

REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = int(getenv("REDIS_PORT"))
REDIS_DB = int(getenv("REDIS_DB"))

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

async def check_redis_connection():
    try:
        pong = await redis_client.ping()
        print("\t\tRedis connection: ", pong)
    except Exception as e:
        print("\t\tError: ", e)

def redis_cache(ttl_seconds: int = 10):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Hash basado en el request (Podría ser el id de sesion por ejemplo o cualquier otra cosa unica, depende del contexto)
            key_raw = f"{func.__name__}:{json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)}"
            key = hashlib.md5(key_raw.encode()).hexdigest()

            # Se busca si existe ese hash en redis, si es así se carga y retorna
            cached = await redis_client.get(key)
            if cached:
                print("Cache hit")
                return json.loads(cached, object_hook=json_util.object_hook)

            print("Cache miss")

            # Se ejecuta la función originalmente llamada
            result = await func(*args, **kwargs)

            # Si no existe se guarda el resultado en Redis con tiempo de expiración (TTL)
            await redis_client.setex(key, ttl_seconds, json.dumps(result, default=json_util.default))
            return result
        return wrapper
    return decorator