from sqlalchemy.orm import Session
from DTOs.requestDtos.task import RequestAddNewTask, RequestEditTask
from api.utils.buckets import get_bucket_by_id, get_bucket_by_name
from db.models.board import Bucket, Task


def get_tasks(db: Session, skip: int = 0, limit: int = 50) -> list[Task]:

  return db.query(Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: str) -> Task:

  return db.query(Task).filter(Task.id == task_id).first()


def get_tasks_related_to_board(db: Session, bucket_id: str) -> list[Task]:

  return db.query(Task).filter(Task.bucket_id == bucket_id).all()


def  create_task(db: Session, bucket_id: str, task: RequestAddNewTask) -> Task:
  bucket = get_bucket_by_id(db, bucket_id)

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


def update_task(db: Session, task: RequestEditTask) -> Task:

  is_bucket_changed = False
  db_task = db.query(Task).filter(Task.id == task.id).first()
  
  if task.title is not None:
    db_task.title = task.title
  
  if task.description is not None:
    db_task.description = task.description
  
  if task.status is not None and task.status is not db_task.status:
    # move to different bucket
    new_bucket = get_bucket_by_name(db, task.status)
    if new_bucket:
      db_task.bucket_id = new_bucket.id
      is_bucket_changed = True
  
  db.commit()
  db.refresh(db_task)
  return (db_task, is_bucket_changed)



def update_both_buckets(db: Session, old_bucket_id: str, new_bucket_id: str):

  new_bucket = get_bucket_by_id(db, new_bucket_id)
  old_bucket = get_bucket_by_id(db, old_bucket_id)

  for index, task in enumerate(new_bucket.tasks):
    task.position = index

  for index, task in enumerate(old_bucket.tasks):
    task.position = index

  db.commit()

