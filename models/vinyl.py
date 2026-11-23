from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, UniqueConstraint

from database.database import Base

from sqlalchemy.orm import relationship

from models.artist import Artist
from models.genre import Genre


class Vinyl(Base):
    __tablename__ = "vinyls"
    __table_args__ = (
        UniqueConstraint("title", "artist_id", name="uq_vinyls_title_artist"),
    )

    id_vinyl = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(String(500), nullable=True)
    artist_id = Column(
        Integer, ForeignKey("artists.id_artist", ondelete="RESTRICT"), nullable=False
    )
    genre_id = Column(
        Integer, ForeignKey("genres.id_genre", ondelete="RESTRICT"), nullable=False
    )
    artist = relationship(Artist)
    genre = relationship(Genre)