from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Esquema base con los datos y validaciones comunes de un artista.
class ArtistBase(BaseModel):

    
    name: str = Field(..., min_length=1, max_length=100)

    
    description: Optional[str] = None

    @field_validator("name", mode="before")
    @classmethod
    def trim_name(cls, value):
        # Recorta espacios antes de comprobar la longitud del nombre.
        if isinstance(value, str):
            return value.strip()

        # Deja que Pydantic informe si el valor no es texto.
        return value

    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, value):
        # Recorta la descripción y convierte el texto vacío en None.
        if isinstance(value, str):
            value = value.strip()
            return value or None

        # Deja que Pydantic valide otros valores, incluido None.
        return value


# Esquema para recibir los datos al crear un artista.
class ArtistCreate(ArtistBase):
    pass


# Esquema para recibir los datos al actualizar un artista.
class ArtistUpdate(ArtistBase):
    pass


# Respuesta breve usada en el listado de artistas.
class ArtistListResponse(BaseModel):
    id_artist: int
    name: str

    # Permite crear la respuesta desde los atributos de un modelo ORM.
    model_config = ConfigDict(from_attributes=True)


# Respuesta completa usada para consultar la ficha de un artista.
class ArtistResponse(ArtistBase):
    id_artist: int

    # Permite crear la respuesta desde los atributos de un modelo ORM.
    model_config = ConfigDict(from_attributes=True)