# 🧪 Database test
# Validates the SQLite engine is alive and the tasks table exists.

from sqlalchemy import inspect, text

from app.db.database import create_tables, engine


def test_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1


def test_task_table_exists():
    create_tables()

    inspector = inspect(engine)

    assert "tasks" in inspector.get_table_names()