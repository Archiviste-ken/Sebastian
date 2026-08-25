# 🧳 Repository package
# 🧳 Contains persistence abstractions for the project domain models.
# 🧳 This package is the bridge between the app's business logic and its SQLite storage.

from sqlalchemy.orm import Session  # 📦 Import Session for type hinting database sessions

from app.db.models import TaskRecord  # 📦 Import TaskRecord ORM model
from app.models.task import Task  # 📦 Import domain Task model


class TaskRepository:  # 🧳 Define the TaskRepository class
    def __init__(self, session: Session):  # 🏗️ Constructor requires a database session
        # 🔌 Keep the database session that this repository will use.
        self.session = session  # 🔌 Store the session as an instance variable

    def create(self, task: Task) -> Task:  # 💾 Define method to create a task in the database
        # 💾 Convert the app task into a database row, then save it.
        record = TaskRecord(  # 🧱 Create a TaskRecord instance
            id=task.id,  # 📝 Copy the ID from the domain task
            goal=task.goal,  # 📝 Copy the goal from the domain task
            status=task.status.value,  # 📝 Extract the string value from the status enum
        )  # 🧱 Close the TaskRecord initialization

        self.session.add(record)  # 💾 Add the new record to the session
        self.session.commit()  # 💾 Commit the transaction to save it

        return task  # ✅ Return the original domain task

    def get(self, task_id: str) -> Task | None:  # 🔎 Define method to retrieve a task by ID
        # 🔎 Find a stored row and turn it back into the app's Task model.
        record = self.session.get(TaskRecord, task_id)  # 🔎 Query the database by primary key

        if record is None:  # 🛡️ Check if no record was found
            return None  # ❌ Return None if the task does not exist

        return Task(  # 🏗️ Reconstruct a domain Task object from the record
            id=record.id,  # 📝 Map the stored ID
            goal=record.goal,  # 📝 Map the stored goal
            status=record.status,  # 📝 Map the stored status string
        )  # 🏗️ Close the domain Task instantiation
