from sqlalchemy import Column, Integer, String, Text

from database.database import Base


class Artist(Base):
    __tablename__ = "artists"

    id_artist = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)