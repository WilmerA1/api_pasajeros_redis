import asyncio
from os import getenv
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    """
    Este script prueba la conexión a MongoDB y intenta leer un documento.
    """
    print("--- Iniciando prueba de conexión a MongoDB ---")
    
    # 1. Cargar variables de entorno desde el archivo .env
    load_dotenv()
    mongo_uri = getenv("MONGO_URI")
    mongo_db_name = getenv("MONGO_DB_NAME")

    if not mongo_uri or not mongo_db_name:
        print("\n[ERROR] No se encontraron las variables MONGO_URI o MONGO_DB_NAME.")
        print("Asegúrate de que tu archivo .env está correcto.")
        return

    print(f"Intentando conectar a: {mongo_uri}")
    print(f"Base de datos: {mongo_db_name}")

    try:
        # 2. Crear el cliente de MongoDB
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # El siguiente comando fuerza la conexión y fallará si no se puede conectar
        await client.server_info() 
        print("\n[ÉXITO] Conexión a MongoDB establecida correctamente.")

        # 3. Intentar leer datos
        db = client[mongo_db_name]
        collection = db.passengers # El nombre de tu colección
        
        print(f"Intentando leer un documento de la colección '{collection.name}'...")
        documento = await collection.find_one()

        if documento:
            print("[ÉXITO] Se encontró un documento:")
            print(documento)
        else:
            print("\n[ADVERTENCIA] La conexión fue exitosa, pero no se encontraron documentos en la colección 'passengers'.")
            print("Verifica que los datos se importaron correctamente con mongoimport.")

    except Exception as e:
        print("\n[ERROR] Falló la conexión o la consulta a MongoDB.")
        print("Detalles del error:", e)
    
    finally:
        if 'client' in locals():
            client.close()
        print("\n--- Prueba finalizada ---")

if __name__ == "__main__":
    asyncio.run(main())