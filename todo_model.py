import uuid
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

class TaskStatus(Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"

@dataclass
class Task:
    description: str
    schedule_for: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = TaskStatus.TODO

class TaskModel:
    def __init__(self, repository):
        self.repository = repository

    def add_task(self, description: str, schedule_for: datetime) -> Task:
        task = Task(description=description, schedule_for=schedule_for)
        return self.repository.add(task)

    def get_all_tasks(self) -> List[Task]:
        return self.repository.get_all()

    def get_task_by_id(self, task_id_str: str) -> Optional[Task]:
        return self.repository.get_by_id_prefix(task_id_str)

    def filter_by_status(self, status: TaskStatus) -> List[Task]:
        return self.repository.get_by_status(status)

    def update_task_status(self, task_id_str: str, new_status: TaskStatus) -> bool:
        task = self.get_task_by_id(task_id_str)
        if task:
            return self.repository.update_status(str(task.id), new_status)
        return False
        
    def update_task_description(self, task_id_str: str, new_desc: str) -> bool:
        task = self.get_task_by_id(task_id_str)
        if task:
            return self.repository.update_description(str(task.id), new_desc)
        return False

    def delete_task(self, task_id_str: str) -> bool:
        task = self.get_task_by_id(task_id_str)
        if task:
            return self.repository.delete(str(task.id))
        return False