from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models.vinyl import Vinyl
from models.artist import Artist
from models.genre import Genre
from schemas.vinyl import VinylCreate, VinylUpdate


def _format_vinyl(vinyl: Vinyl) -> dict:
    """Convierte un vinilo y sus relaciones a datos listos para la respuesta."""
    return {
        "id_vinyl": vinyl.id_vinyl,
        "title": vinyl.title,
        "year": vinyl.year,
        "price": format(Decimal(vinyl.price), ".2f"),
        "description": vinyl.description,
        "artist_id": vinyl.artist_id,
        "genre_id": vinyl.genre_id,
        "artist": {
            "id_artist": vinyl.artist.id_artist,
            "name": vinyl.artist.name,
        },
        "genre": {
            "id_genre": vinyl.genre.id_genre,
            "name": vinyl.genre.name,
        },
    }


def get_vinyls(
    db: Session,
    artist: str | None = None,
    title: str | None = None,
) -> list[dict]:
    """Devuelve vinilos y aplica los filtros recibidos, si los hay."""
    statement = (
        select(Vinyl)
        .options(joinedload(Vinyl.artist), joinedload(Vinyl.genre))
        .order_by(Vinyl.id_vinyl)
    )

    if artist and artist.strip():
        statement = statement.join(Vinyl.artist).where(
            Vinyl.artist.property.mapper.class_.name.ilike(
                f"%{artist.strip()}%"
            )
        )

    if title and title.strip():
        statement = statement.where(Vinyl.title.ilike(f"%{title.strip()}%"))

    vinyls = db.scalars(statement).all()

    return [_format_vinyl(vinyl) for vinyl in vinyls]


def get_vinyl_by_id(db: Session, vinyl_id: int) -> dict | None:
    """Busca un vinilo por su ID e incluye su artista y género."""
    statement = (
        select(Vinyl)
        .options(joinedload(Vinyl.artist), joinedload(Vinyl.genre))
        .where(Vinyl.id_vinyl == vinyl_id)
    )

    vinyl = db.scalars(statement).first()

    if vinyl is None:
        return None

    return _format_vinyl(vinyl)

def _validate_relations(db: Session, artist_id: int, genre_id: int) -> None:
    if db.get(Artist, artist_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el artista con id {artist_id}",
        )

    if db.get(Genre, genre_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el género con id {genre_id}",
        )


def _validate_unique_title(
    db: Session,
    title: str,
    artist_id: int,
    exclude_vinyl_id: int | None = None,
) -> None:
    statement = select(Vinyl).where(
        Vinyl.title == title,
        Vinyl.artist_id == artist_id,
    )

    if exclude_vinyl_id is not None:
        statement = statement.where(Vinyl.id_vinyl != exclude_vinyl_id)

    existing_vinyl = db.scalars(statement).first()

    if existing_vinyl is not None:
        raise HTTPException(
            status_code=409,
            detail="Ese artista ya tiene un vinilo con ese título",
        )


def create_vinyl(db: Session, vinyl_data: VinylCreate) -> Vinyl:
    data = vinyl_data.model_dump()

    _validate_relations(db, data["artist_id"], data["genre_id"])
    _validate_unique_title(db, data["title"], data["artist_id"])

    vinyl = Vinyl(**data)
    db.add(vinyl)

    try:
        db.commit()
        db.refresh(vinyl)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo crear el vinilo por un conflicto con los datos",
        )

    return vinyl


def update_vinyl(
    db: Session,
    vinyl_id: int,
    vinyl_data: VinylUpdate,
) -> Vinyl:
    vinyl = db.get(Vinyl, vinyl_id)

    if vinyl is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el vinilo con id {vinyl_id}",
        )

    data = vinyl_data.model_dump()

    _validate_relations(db, data["artist_id"], data["genre_id"])
    _validate_unique_title(
        db,
        data["title"],
        data["artist_id"],
        exclude_vinyl_id=vinyl_id,
    )

    for field, value in data.items():
        setattr(vinyl, field, value)

    try:
        db.commit()
        db.refresh(vinyl)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo actualizar el vinilo por un conflicto con los datos",
        )

    return vinyl


def delete_vinyl(db: Session, vinyl_id: int) -> None:
    vinyl = db.get(Vinyl, vinyl_id)

    if vinyl is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el vinilo con id {vinyl_id}",
        )

    try:
        db.delete(vinyl)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo borrar el vinilo por una restricción de la base de datos",
        )