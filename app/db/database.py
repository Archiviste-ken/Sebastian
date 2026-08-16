from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base


DATABASE_URL = "sqlite:///./sebastian.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)