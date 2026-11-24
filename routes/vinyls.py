from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from controllers.vinyls_controller import get_vinyl_by_id, get_vinyls
from database.database import get_db


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