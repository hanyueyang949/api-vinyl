from sqlite3 import (
    SQLITE_CONSTRAINT_FOREIGNKEY,
    SQLITE_CONSTRAINT_TRIGGER,
    SQLITE_CONSTRAINT_UNIQUE,
)

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.artist import Artist
from schemas.artist import ArtistCreate, ArtistUpdate


def list_artists(db: Session) -> list[Artist]:
    return list(db.scalars(select(Artist).order_by(Artist.id_artist)))


def get_artist(db: Session, id_artist: int) -> Artist:
    artist = db.get(Artist, id_artist)
    if artist is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Artist not found")
    return artist


def _save_artist(db: Session, artist: Artist) -> Artist:
    db.add(artist)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if getattr(error.orig, "sqlite_errorcode", None) == SQLITE_CONSTRAINT_UNIQUE:
            raise HTTPException(
                status.HTTP_409_CONFLICT, "Artist name already exists"
            ) from error
        raise
    db.refresh(artist)
    return artist


def create_artist(db: Session, data: ArtistCreate) -> Artist:
    return _save_artist(db, Artist(name=data.name, description=data.description))


def update_artist(db: Session, id_artist: int, data: ArtistUpdate) -> Artist:
    artist = get_artist(db, id_artist)
    artist.name = data.name
    artist.description = data.description
    return _save_artist(db, artist)


def delete_artist(db: Session, id_artist: int) -> None:
    artist = get_artist(db, id_artist)
    db.delete(artist)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if getattr(error.orig, "sqlite_errorcode", None) in (
            SQLITE_CONSTRAINT_FOREIGNKEY,
            SQLITE_CONSTRAINT_TRIGGER,
        ):
            raise HTTPException(
                status.HTTP_409_CONFLICT, "Artist has linked vinyl records"
            ) from error
        raise