from sqlite3 import (
    SQLITE_CONSTRAINT_FOREIGNKEY,
    SQLITE_CONSTRAINT_TRIGGER,
    SQLITE_CONSTRAINT_UNIQUE,
)

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.genre import Genre
from schemas.genre import GenreCreate, GenreUpdate


def list_genres(db: Session) -> list[Genre]:
    return list(db.scalars(select(Genre).order_by(Genre.id_genre)))


def get_genre(db: Session, id_genre: int) -> Genre:
    genre = db.get(Genre, id_genre)
    if genre is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Genre not found")
    return genre


def _save_genre(db: Session, genre: Genre) -> Genre:
    db.add(genre)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if getattr(error.orig, "sqlite_errorcode", None) == SQLITE_CONSTRAINT_UNIQUE:
            raise HTTPException(
                status.HTTP_409_CONFLICT, "Genre name already exists"
            ) from error
        raise
    db.refresh(genre)
    return genre


def create_genre(db: Session, data: GenreCreate) -> Genre:
    return _save_genre(db, Genre(name=data.name))


def update_genre(db: Session, id_genre: int, data: GenreUpdate) -> Genre:
    genre = get_genre(db, id_genre)
    genre.name = data.name
    return _save_genre(db, genre)


def delete_genre(db: Session, id_genre: int) -> None:
    genre = get_genre(db, id_genre)
    db.delete(genre)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if getattr(error.orig, "sqlite_errorcode", None) in (
            SQLITE_CONSTRAINT_FOREIGNKEY,
            SQLITE_CONSTRAINT_TRIGGER,
        ):
            raise HTTPException(
                status.HTTP_409_CONFLICT, "Genre has linked vinyl records"
            ) from error
        raise