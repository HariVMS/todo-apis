from sqlalchemy.orm import Session
from src.models.todo import TaskDB, Status
from datetime import datetime
from src.schemas.todo import Task

# CRUD: Create Task
def create_task(db: Session, task: Task):
    db_task = TaskDB(
        task_name=task.task_name,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
        created_at=datetime.now(),
        duration=str(task.duration),
        priority=task.priority,
        labels=list(task.labels),
        extra_metadata=task.extra_metadata,
        participants=task.participants,
        is_urgent=task.is_urgent
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# CRUD: Get Task by ID
def get_task(db: Session, task_id: int):
    return db.query(TaskDB).filter(TaskDB.task_id == task_id).first()

# CRUD: Get all Tasks
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TaskDB).offset(skip).limit(limit).all()

# CRUD: Update Task
def update_task(db: Session, task_id: int, task: Task):
    db_task = db.query(TaskDB).filter(TaskDB.task_id == task_id).first()
    if db_task:
        db_task.task_name = task.task_name
        db_task.description = task.description
        db_task.status = task.status
        db_task.due_date = task.due_date
        db_task.duration = str(task.duration)
        db_task.priority = task.priority
        db_task.labels = list(task.labels)
        db_task.extra_metadata = task.extra_metadata
        db_task.participants = task.participants
        db_task.is_urgent = task.is_urgent
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

# CRUD: Delete Task
def delete_task(db: Session, task_id: int):
    db_task = db.query(TaskDB).filter(TaskDB.task_id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return db_task
    return None
