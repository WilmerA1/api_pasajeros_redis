#Pasajeros Service
import asyncio
from app.cache.redis import redis_cache
from app.db.mongo import db
from app.models.ruta_model import RutaModel
from typing import List
from dotenv import load_dotenv
from os import getenv
load_dotenv() 

from pydantic import ValidationError 


REDIS_TTL = int(getenv("REDIS_TTL"))

@redis_cache(ttl_seconds=REDIS_TTL)
async def get_all_rutas() -> List[RutaModel]:
    await asyncio.sleep(2)  # Simulamos que la operacion tarda mucho tiempo
    rutas = await db.passengers.find().to_list(length=None)
    return rutas

async def get_ruta(codigo_ruta: str) -> RutaModel:
    ruta = await db.passengers.find_one({"codigo_ruta": codigo_ruta})
    return ruta