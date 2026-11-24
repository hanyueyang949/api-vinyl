from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from controllers import artists_controller
from database.database import get_db
from schemas.artist import ArtistCreate, ArtistListResponse, ArtistResponse, ArtistUpdate


router = APIRouter(prefix="/artists", tags=["Artists"])


@router.get("", response_model=list[ArtistListResponse])
def list_artists(db: Session = Depends(get_db)):
    return artists_controller.list_artists(db)


@router.get("/{id_artist}", response_model=ArtistResponse)
def get_artist(id_artist: int, db: Session = Depends(get_db)):
    return artists_controller.get_artist(db, id_artist)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ArtistResponse)
def create_artist(data: ArtistCreate, db: Session = Depends(get_db)):
    return artists_controller.create_artist(db, data)


@router.put("/{id_artist}", response_model=ArtistResponse)
def update_artist(id_artist: int, data: ArtistUpdate, db: Session = Depends(get_db)):
    return artists_controller.update_artist(db, id_artist, data)


@router.delete("/{id_artist}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artist(id_artist: int, db: Session = Depends(get_db)) -> None:
    artists_controller.delete_artist(db, id_artist)