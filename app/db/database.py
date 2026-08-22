# 🗄️ Database bootstrap
# This file initializes the SQLite database used by Sebastian's persistence layer.
# It creates the engine and ensures the schema is present before requests run.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base


# 📍 Local SQLite database path for the project.
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
    # 🏗️ Create all mapped database tables if they do not already exist.
    Base.metadata.create_all(bind=engine)