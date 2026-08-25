# 🧱 ORM models
# 🧱 SQLAlchemy models map Sebastian's domain objects into database tables.
# 🧱 This file defines the persistence representation of a task.

from sqlalchemy import String  # 📦 Import String column type from sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # 📦 Import ORM tools for declarative models


class Base(DeclarativeBase):  # 🧱 Define the Base class for all ORM models
    # 🧩 Common base for all ORM models.
    pass  # 🧱 Pass to leave the class body empty as it just serves as a base


class TaskRecord(Base):  # 🧱 Define the TaskRecord model inheriting from Base
    # 📋 Table name for stored tasks.
    __tablename__ = "tasks"  # 💾 Set the database table name to 'tasks'

    # 🆔 Task identifier stored as the primary key.
    id: Mapped[str] = mapped_column(  # 📝 Define the 'id' column as a string
        String,  # 💾 Use the String type
        primary_key=True,  # 🔑 Mark this column as the primary key
    )  # 📝 Close the column definition

    # 🎯 The task goal as text.
    goal: Mapped[str] = mapped_column(  # 📝 Define the 'goal' column as a string
        String,  # 💾 Use the String type
        nullable=False,  # 🛡️ Ensure this column cannot be null
    )  # 📝 Close the column definition

    # 🔄 Current lifecycle state of the task.
    status: Mapped[str] = mapped_column(  # 📝 Define the 'status' column as a string
        String,  # 💾 Use the String type
        nullable=False,  # 🛡️ Ensure this column cannot be null
    )  # 📝 Close the column definition