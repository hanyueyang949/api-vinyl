from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config.config_variables import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

def compare_casefolded_text(left: str, right: str) -> int:
    left_key = left.casefold()
    right_key = right.casefold()

    if left_key < right_key:
        return -1
    if left_key > right_key:
        return 1
    return 0


@event.listens_for(engine, "connect")
def configure_sqlite_connection(connection, record):
    connection.create_collation("UNICODE_NOCASE", compare_casefolded_text)

    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()