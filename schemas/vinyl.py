from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


# Esquema base para los datos que se reciben de un vinilo.
class VinylBase(BaseModel):

    title: str = Field(..., min_length=1, max_length=150)
    year: int = Field(..., gt=0, strict=True)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    artist_id: int = Field(..., gt=0, strict=True)
    genre_id: int = Field(..., gt=0, strict=True)


    @field_validator("title", mode="before")
    @classmethod
    def trim_title(cls, value):
        # Recorta los espacios antes de comprobar la longitud.
        if isinstance(value, str):
            return value.strip()

        # Deja que Pydantic informe si el valor no es texto.
        return value
    
    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, value):
        # Recorta los espacios y convierte el texto vacío en None.
        if isinstance(value, str):
            value = value.strip()
            return value or None

        # Deja que Pydantic valide otros valores.
        return value

# Datos necesarios para crear un vinilo.
class VinylCreate(VinylBase):
    pass

# Datos necesarios para actualizar todos los datos de un vinilo.
class VinylUpdate(VinylBase):
    pass

# Datos que muestra la API en la ficha de un vinilo.
class VinylResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_vinyl: int
    title: str
    year: int
    description: Optional[str]
    price: Decimal
    artist_id: int
    genre_id: int

    @field_serializer("price", return_type=str)
    def serialize_price(self, value: Decimal) -> str:
        return format(value, ".2f")