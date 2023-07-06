from sqlalchemy.orm import Session
from DTOs.requestDtos.task import RequestAddNewTask, RequestEditTask
from api.utils.buckets import get_bucket_by_id, get_bucket_by_name
from db.models.board import Board, Bucket, Task


def get_tasks(db: Session, skip: int = 0, limit: int = 50) -> list[Task]:

  return db.query(Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: str) -> Task:

  return db.query(Task).filter(Task.id == task_id).first()


def get_tasks_related_to_board(db: Session, bucket_id: str) -> list[Task]:

  return db.query(Task).filter(Task.bucket_id == bucket_id).all()


def  create_task(db: Session, bucket_id: str, task: RequestAddNewTask) -> Task:
  bucket = get_bucket_by_id(db, bucket_id)
  position = 0

  if len(bucket.tasks) > 0 and bucket.tasks is not None: 
    position = max(tuple([task.position for task in bucket.tasks])) + 1

  db_task = Task(
    title = task.title,
    description = task.description,
    position = position,
    status = bucket.name,
    bucket_id = bucket_id,
  )

  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  return db_task

def update_task_position(db: Session, bucket_id: str) -> Bucket:

  bucket = db.query(Bucket).filter(Bucket.id == bucket_id).first()

  for index, task in enumerate(sorted(bucket.tasks, key=lambda task: task.position)):
    task.position = index
  
  db.commit()
  return bucket


def update_task(db: Session, task: RequestEditTask) -> Task:

  db_task = db.query(Task).filter(Task.id == task.id).first()
  
  if task.title is not None:
    db_task.title = task.title
  
  if task.description is not None:
    db_task.description = task.description
  
  
  db.commit()
  db.refresh(db_task)
  return db_task


def update_task_bucteks(db: Session, task: RequestEditTask) -> Task:

  db_task = db.query(Task).filter(Task.id == task.id).first()
  
  if task.title is not None:
    db_task.title = task.title
  
  if task.description is not None:
    db_task.description = task.description
  
  if task.status is not None:
    new_bucket = get_bucket_by_name(db, task.status)
    db_task.bucket_id = new_bucket.id
    db_task.position = 1000000
  
  db.commit()
  db.refresh(db_task)
  return db_task


def update_both_buckets(db: Session, new_Bucket_id: str, old_bucket_id: str, task_id: str):

  old_bucket = update_task_position(db, old_bucket_id)
  new_bucket = update_task_position(db, new_Bucket_id)

  for index, task in enumerate(old_bucket.tasks):
    task.position = index

  for index, task in enumerate(new_bucket.tasks):
    if(task.id == task_id):
      task.position = 0
    task.position = index + 1

  db.commit()
  return db.query(Board).filter(Board.is_active == True).first()

