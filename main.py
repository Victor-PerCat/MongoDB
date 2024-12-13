from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
DB_NAME = os.getenv("DB_NAME")

# Construir URI dinámicamente
uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName={DB_NAME}"

# Crear cliente y verificar conexión
try:
    client = MongoClient(uri)
    client.admin.command('ping')  # Confirmar conexión exitosa
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Error al conectar con MongoDB:", e)
    raise e

# Seleccionar la base de datos
db = client[DB_NAME]

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Modelo Pydantic para validación
class ClienteModel(BaseModel):
    nombre: str
    correo: str
    telefono: str
    direccion: dict
    fecha_registro: str

# Rutas CRUD
@app.post("/clientes/")
async def crear_cliente(cliente: ClienteModel):
    cliente_dict = cliente.dict()
    resultado = db.clientes.insert_one(cliente_dict)
    if resultado.inserted_id:
        return {"id": str(resultado.inserted_id), "mensaje": "Cliente creado exitosamente"}
    raise HTTPException(status_code=500, detail="Error al crear el cliente")

@app.get("/clientes/{id}")
async def obtener_cliente(id: str):
    cliente = db.clientes.find_one({"_id": id})
    if cliente:
        return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.put("/clientes/{id}")
async def actualizar_cliente(id: str, cliente: ClienteModel):
    resultado = db.clientes.update_one({"_id": id}, {"$set": cliente.dict()})
    if resultado.modified_count:
        return {"mensaje": "Cliente actualizado exitosamente"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.delete("/clientes/{id}")
async def eliminar_cliente(id: str):
    resultado = db.clientes.delete_one({"_id": id})
    if resultado.deleted_count:
        return {"mensaje": "Cliente eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")
@app.get("/")
async def read_root():
    return {"mensaje": "Bienvenido a la API de Clientes"}

@app.get("/favicon.ico")
async def favicon():
    return {"mensaje": "No hay favicon disponible"}

