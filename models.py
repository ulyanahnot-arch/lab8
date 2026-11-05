import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from todo_model import TaskStatus 

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    schedule_for = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO)