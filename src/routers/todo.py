from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.crud.todo import create_task,get_task,get_tasks,update_task,delete_task # assuming task models and schemas are in these files
from src.schemas.todo import Task,TaskResponseModel # assuming task models and schemas are in these files
from typing import List
from src.models.todo import TaskDB
from src.core.database import get_db  # get_db is a function that provides a DB session

router = APIRouter()

# Route to create a task
@router.post("/tasks/")
def create_tasks(task: Task, db: Session = Depends(get_db)):
    db_task = create_task(db=db, task=task)
    return db_task

# Route to get task by ID
@router.get("/tasks/{task_id}", response_model=TaskResponseModel)
def get_task_single(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# Route to get all tasks
@router.get("/tasks/", response_model=List[TaskResponseModel])
def get_tasks_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks

# Route to update a task
@router.put("/tasks/{task_id}", response_model=TaskResponseModel)
def update_task_single(task_id: int, task: Task, db: Session = Depends(get_db)):
    db_task = update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# Route to delete a task
@router.delete("/tasks/{task_id}", response_model=TaskResponseModel)
def delete_task_single(task_id: int, db: Session = Depends(get_db)):
    db_task = delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
