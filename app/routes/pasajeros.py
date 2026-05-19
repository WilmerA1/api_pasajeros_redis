from fastapi import APIRouter, HTTPException
from typing import List
from app.cache.redis import check_redis_connection, redis_cache
from app.models.ruta_model import RutaModel
from app.db.mongo import db
from dotenv import load_dotenv
from os import getenv
load_dotenv()
import asyncio

from app.services import pasajeros_service

REDIS_TTL = int(getenv("REDIS_TTL"))

pasajeros = APIRouter(
    prefix="/pasajeros",
    tags=["Pasajeros"]
)

@pasajeros.get("/", response_model=List[RutaModel])
async def obtener_rutas():
    """Obtiene todas las rutas desde MongoDB."""
    try:
        rutas = await pasajeros_service.get_all_rutas()
        return rutas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pasajeros.get("/{codigo_ruta}", response_model=RutaModel)
async def obtener_ruta_por_codigo(codigo_ruta: str):
    """Obtiene una ruta específica según su código."""
    ruta = await pasajeros_service.get_ruta(codigo_ruta)
    if ruta:
        return ruta
    raise HTTPException(status_code=404, detail="Ruta no encontrada")



######### RUTA DE PRUEBA ##########
@pasajeros.get("/cached/", response_model=int)
async def obtener_rutas():
    return await test()

@redis_cache(ttl_seconds=REDIS_TTL)
async def test():
    await asyncio.sleep(2)
    return 42