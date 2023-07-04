from sqlalchemy.orm import Session
from DTOs.requestDtos.task import RequestAddNewTask
from api.utils.buckets import get_bucket_by_id
from db.models.board import Bucket, Task


def get_tasks(db: Session, skip: int = 0, limit: int = 50) -> list[Task]:

  return db.query(Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: str) -> Task:

  return db.query(Task).filter(Task.id == task_id).first()


def get_tasks_related_to_board(db: Session, bucket_id: str) -> list[Task]:

  return db.query(Task).filter(Task.bucket_id == bucket_id).all()


def  create_task(db: Session, bucket_id: str, task: RequestAddNewTask) -> Task:
  bucket = get_bucket_by_id(db, id = bucket_id)

  db_task = Task(
    title = task.title,
    description = task.description,
    position = 0,
    status = bucket.name,
    bucket_id = bucket_id,
  )

  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  return db_task

def update_task_position(db: Session, bucket_id: str):

  tasks = db.query(Task).filter(Task.bucket_id == bucket_id).all()

  for index, task in enumerate(tasks):
    task.position = index
  
  db.commit()
