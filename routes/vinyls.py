from fastapi import APIRouter, Depends, HTTPException, Query,  Response, status
from sqlalchemy.orm import Session

from controllers.vinyls_controller import get_vinyl_by_id, get_vinyls
from database.database import get_db

from controllers.vinyls_controller import (
    create_vinyl,
    delete_vinyl,
    update_vinyl,
)
from schemas.vinyl import VinylCreate, VinylResponse, VinylUpdate


router = APIRouter(
    prefix="/vinyls",
    tags=["Vinyls"],
)


@router.get("")
def list_vinyls(
    artist: str | None = Query(default=None, description="Filtra por nombre de artista"),
    title: str | None = Query(default=None, description="Filtra por título del vinilo"),
    db: Session = Depends(get_db),
):
    """Lista los vinilos; permite filtrar por artista y título."""
    return get_vinyls(db=db, artist=artist, title=title)


@router.get("/{vinyl_id}")
def read_vinyl(
    vinyl_id: int,
    db: Session = Depends(get_db),
):
    """Devuelve el detalle de un vinilo o un error 404 si no existe."""
    vinyl = get_vinyl_by_id(db=db, vinyl_id=vinyl_id)

    if vinyl is None:
        raise HTTPException(
            status_code=404,
            detail="Vinilo no encontrado",
        )

    return vinyl

@router.post(
    "",
    response_model=VinylResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vinyl_route(
    vinyl_data: VinylCreate,
    db: Session = Depends(get_db),
):
    return create_vinyl(db=db, vinyl_data=vinyl_data)


@router.put(
    "/{vinyl_id}",
    response_model=VinylResponse,
    status_code=status.HTTP_200_OK,
)
def update_vinyl_route(
    vinyl_id: int,
    vinyl_data: VinylUpdate,
    db: Session = Depends(get_db),
):
    return update_vinyl(
        db=db,
        vinyl_id=vinyl_id,
        vinyl_data=vinyl_data,
    )


@router.delete(
    "/{vinyl_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vinyl_route(
    vinyl_id: int,
    db: Session = Depends(get_db),
):
    delete_vinyl(db=db, vinyl_id=vinyl_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)