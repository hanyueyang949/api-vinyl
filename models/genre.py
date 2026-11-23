from sqlalchemy import Column, Integer, String

from database.database import Base


class Genre(Base):
    __tablename__ = "genres"

    id_genre = Column(Integer, primary_key=True)
    name = Column(String(100, collation="UNICODE_NOCASE"), nullable=False, unique=True)