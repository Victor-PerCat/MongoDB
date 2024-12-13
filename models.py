from pydantic import BaseModel

class Cliente(BaseModel):
    nombre: str
    correo: str
    telefono: str
    direccion: dict
    fecha_registro: str