from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId
from pydantic import BeforeValidator
from typing import Annotated

PyObjectIdType = Annotated[str, BeforeValidator(lambda v: str(v) if ObjectId.is_valid(v) else ValueError("Invalid ObjectId"))]

class RutaModel(BaseModel):
    id: Optional[PyObjectIdType] = Field(default=None, alias="_id")
    nombre_operador: str
    cedula: str
    codigo_ruta: str
    descripcion_ruta: str
    codigo_ramal: str
    descripcion_ramal: Optional[str] = None
    mes: int
    anno: int
    pasajero_equivalente: Optional[float] = None
    pasajerosTotal: Optional[str] = None
    
    pasajeros_adulto_mayor: int
    pasajeros_regulares: int
    carreras: float
    ingresos: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        from_attributes=True,
    )