from sqlalchemy import Column, Integer, String, Date, Time, Enum, Boolean, JSON, Text, Float,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum

Base = declarative_base()

# Enum for Task Status
class Status(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

# Enum for Task Types
class TaskType(enum.Enum):
    personal = "personal"
    work = "work"
    urgent = "urgent"
    other = "other"

class TaskDB(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(Status), default=Status.pending)
    due_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    duration = Column(String, nullable=False)  # ISO 8601 format
    priority = Column(Integer, nullable=False)
    labels = Column(JSON, default=[])  # List of labels
    extra_metadata = Column(JSON, default={})  # Additional metadata
    participants = Column(JSON, default=[])  # List of participant emails
    is_urgent = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Task(task_name={self.task_name}, due_date={self.due_date}, priority={self.priority})>"
