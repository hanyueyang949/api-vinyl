from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models.vinyl import Vinyl


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