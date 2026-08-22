# 🧱 ORM models
# SQLAlchemy models map Sebastian's domain objects into database tables.
# This file defines the persistence representation of a task.

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    # 🧩 Common base for all ORM models.
    pass


class TaskRecord(Base):
    # 📋 Table name for stored tasks.
    __tablename__ = "tasks"

    # 🆔 Task identifier stored as the primary key.
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    # 🎯 The task goal as text.
    goal: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # 🔄 Current lifecycle state of the task.
    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )