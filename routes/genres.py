from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from controllers import genres_controller
from database.database import get_db
from schemas.genre import GenreCreate, GenreResponse, GenreUpdate


router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("", response_model=list[GenreResponse])
def list_genres(db: Session = Depends(get_db)):
    return genres_controller.list_genres(db)


@router.get("/{id_genre}", response_model=GenreResponse)
def get_genre(id_genre: int, db: Session = Depends(get_db)):
    return genres_controller.get_genre(db, id_genre)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=GenreResponse)
def create_genre(data: GenreCreate, db: Session = Depends(get_db)):
    return genres_controller.create_genre(db, data)


@router.put("/{id_genre}", response_model=GenreResponse)
def update_genre(id_genre: int, data: GenreUpdate, db: Session = Depends(get_db)):
    return genres_controller.update_genre(db, id_genre, data)


@router.delete("/{id_genre}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(id_genre: int, db: Session = Depends(get_db)) -> None:
    genres_controller.delete_genre(db, id_genre)