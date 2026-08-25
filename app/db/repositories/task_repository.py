# 🧳 Task repository
# 🧳 This repository handles task persistence between the domain model and SQLite.

from sqlalchemy.orm import Session  # 📦 Import Session for type hinting

from app.db.models import TaskRecord  # 📦 Import the TaskRecord ORM model
from app.models.task import Task  # 📦 Import the domain Task model


class TaskRepository:  # 🧳 Define the TaskRepository class
    def __init__(self, session: Session):  # 🏗️ Constructor requires a database session
        # 🧵 SQLAlchemy session used for database operations.
        self.session = session  # 🔌 Store the database session

    def create(self, task: Task) -> Task:  # 💾 Define method to create a new task
        # 📝 Convert the domain task into a database record and save it.
        record = TaskRecord(  # 🧱 Create a TaskRecord instance
            id=task.id,  # 📝 Assign the ID
            goal=task.goal,  # 📝 Assign the goal
            status=task.status.value,  # 📝 Assign the enum value of the status
        )  # 🧱 Close TaskRecord creation

        self.session.add(record)  # 💾 Stage the record for insertion
        self.session.commit()  # 💾 Commit the transaction to the database

        return task  # ✅ Return the domain task

    def get(self, task_id: str) -> Task | None:  # 🔎 Define method to fetch a task
        # 🔎 Retrieve a task by ID and convert it back into a domain object.
        record = self.session.get(TaskRecord, task_id)  # 🔎 Fetch the record by its primary key

        if record is None:  # 🛡️ Check if the query returned nothing
            return None  # ❌ Return None to indicate missing task

        return Task(  # 🏗️ Reconstruct the domain Task object
            id=record.id,  # 📝 Assign the ID from the record
            goal=record.goal,  # 📝 Assign the goal from the record
            status=record.status,  # 📝 Assign the status from the record
        )  # 🏗️ Close the domain Task instantiation