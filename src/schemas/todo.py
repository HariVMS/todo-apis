from pydantic import BaseModel, Field, validator
from datetime import datetime, date, timedelta
from dateutil import parser as date_parser
from typing import Optional, Set, Dict, List
from enum import Enum

# Enum for Task Status
class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

# Enum for Task Types
class TaskType(str, Enum):
    personal = "personal"
    work = "work"
    urgent = "urgent"
    other = "other"

class Task(BaseModel):
    task_id: int = Field(..., ge=1, description="Unique identifier for the task")
    task_name: str = Field(..., max_length=100, description="The name of the task")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the task")
    status: Status = Field(..., description="Status of the task")
    due_date: date = Field(..., description="Due date for the task in dd/mm/yyyy format")
    duration: timedelta = Field(..., description="Estimated duration of the task")
    priority: int = Field(..., ge=1, le=5, description="Priority level from 1 (low) to 5 (high)")
    labels: Set[str] = Field(default_factory=set, description="Set of labels for categorization")
    extra_metadata: Dict[str, str] = Field(default_factory=dict, description="Additional metadata")
    participants: List[str] = Field(default_factory=list, description="List of participants' email addresses")
    is_urgent: bool = Field(default=False, description="Indicates if the task is urgent")

    # Updated validator for date fields
    @validator('due_date', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                parsed_date = date_parser.parse(value, dayfirst=True)  # Supports 'dd/mm/yyyy' format
                return parsed_date.date()
            except (ValueError, TypeError):
                raise ValueError("Invalid date format. Expected 'dd/mm/yyyy' format.")
        return value

    # Validator to ensure the due_date is in the future
    @validator('due_date')
    def due_date_in_future(cls, value):
        if value < date.today():
            raise ValueError("Due date must be in the future")
        return value

    # Root validator for interdependent validation logic (example)
    @validator('priority')
    def check_priority_for_in_progress(cls, priority, values):
        status = values.get('status')
        if status == "in_progress" and priority < 2:
            raise ValueError("Priority must be at least 2 for in-progress tasks.")
        return priority

    # Validator for duration field
    # Validator for duration field
@validator("duration", pre=True)
def parse_timedelta(cls, value):
    if isinstance(value, str):
        try:
            # Parse duration from string format if needed
            days, time_part = value.split(' days, ')
            hours, minutes, seconds = map(int, time_part.split(':'))
            return timedelta(days=int(days), hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            raise ValueError("Invalid duration format")
    return value  # Return raw timedelta object if already in timedelta format

class TaskResponseModel(BaseModel):
    task_id: int
    task_name: str
    description: Optional[str]
    status: Status
    due_date: date
    duration: str  # String type for duration
    priority: int
    labels: Set[str]
    extra_metadata: Dict[str, str]
    participants: List[str]
    is_urgent: bool

    @classmethod
    def from_task(cls, task: Task):
        duration_str = f"{task.duration.days} days, {task.duration.seconds//3600}:{(task.duration.seconds//60)%60:02}:{task.duration.seconds%60:02}"
        return cls(**task.dict(), duration=duration_str)