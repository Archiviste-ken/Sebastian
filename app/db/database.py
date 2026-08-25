# 🗄️ Database bootstrap
# 🗄️ This file initializes the SQLite database used by Sebastian's persistence layer.
# 🗄️ It creates the engine and ensures the schema is present before requests run.

from sqlalchemy import create_engine  # 📦 Import create_engine to connect to the database
from sqlalchemy.orm import sessionmaker  # 📦 Import sessionmaker to construct Session classes

from app.db.models import Base  # 📦 Import the declarative Base from models


# 📍 Local SQLite database path for the project.
DATABASE_URL = "sqlite:///./sebastian.db"  # 🔧 Set the connection string for SQLite

engine = create_engine(  # 💾 Create the SQLAlchemy engine instance
    DATABASE_URL,  # 💾 Pass the database URL
    connect_args={"check_same_thread": False},  # 🔧 Allow multithreading for SQLite
)  # 💾 Close the engine creation

SessionLocal = sessionmaker(  # 💾 Create a configured Session class
    bind=engine,  # 💾 Bind the session to the engine
    autoflush=False,  # 🔧 Disable automatic flushing
    autocommit=False,  # 🔧 Disable automatic commits
)  # 💾 Close the sessionmaker


def create_tables() -> None:  # 🏗️ Define function to initialize database schema
    # 🏗️ Create all mapped database tables if they do not already exist.
    Base.metadata.create_all(bind=engine)  # 💾 Issue CREATE TABLE statements to the database