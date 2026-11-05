from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import cast, String
from models import TaskDB
from todo_model import Task, TaskStatus

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, task_db: TaskDB) -> Task:
        return Task(
            description=task_db.description,
            schedule_for=task_db.schedule_for,
            id=task_db.id,
            created_at=task_db.created_at,
            status=task_db.status
        )

    def add(self, task: Task) -> Task:
        task_db = TaskDB(
            id=task.id,
            description=task.description,
            schedule_for=task.schedule_for,
            created_at=task.created_at,
            status=task.status
        )
        self.session.add(task_db)
        self.session.commit()
        return task

    def get_all(self) -> List[Task]:
        tasks_db = self.session.query(TaskDB).all()
        return [self._to_domain(t) for t in tasks_db]

    def get_by_id_prefix(self, task_id_str: str) -> Optional[Task]:
        task_db = self.session.query(TaskDB).filter(cast(TaskDB.id, String).startswith(task_id_str)).first()
        if task_db:
            return self._to_domain(task_db)
        return None

    def get_by_status(self, status: TaskStatus) -> List[Task]:
        tasks_db = self.session.query(TaskDB).filter(TaskDB.status == status).all()
        return [self._to_domain(t) for t in tasks_db]

    def update_status(self, task_id: str, new_status: TaskStatus) -> bool:
        task_db = self.session.query(TaskDB).filter(cast(TaskDB.id, String) == task_id).first()
        if task_db:
            task_db.status = new_status
            self.session.commit()
            return True
        return False

    def update_description(self, task_id: str, new_desc: str) -> bool:
        task_db = self.session.query(TaskDB).filter(cast(TaskDB.id, String) == task_id).first()
        if task_db:
            task_db.description = new_desc
            self.session.commit()
            return True
        return False

    def delete(self, task_id: str) -> bool:
        task_db = self.session.query(TaskDB).filter(cast(TaskDB.id, String) == task_id).first()
        if task_db:
            self.session.delete(task_db)
            self.session.commit()
            return True
        return False