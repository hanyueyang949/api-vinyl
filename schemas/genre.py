from pydantic import BaseModel, ConfigDict, Field, field_validator

# Esquema base para los datos de un género.
class GenreBase(BaseModel):
    
    name: str = Field(..., min_length=1, max_length=100)

    @field_validator("name", mode="before")
    @classmethod
    def trim_name(cls, value):
        # Quita los espacios de los extremos antes de validar.
        if isinstance(value, str):
            return value.strip()

        # Deja que Pydantic informe si el valor no es texto.
        return value

# Datos que recibe la API al crear un género.
class GenreCreate(GenreBase):
    pass


# Datos que recibe la API al actualizar un género.
class GenreUpdate(GenreBase):
    pass


# Datos que devuelve la API en el listado y la ficha del género.
class GenreResponse(GenreBase):
    id_genre: int

    # Permite crear la respuesta desde un modelo de SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)