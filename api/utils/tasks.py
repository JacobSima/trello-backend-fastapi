from sqlalchemy.orm import Session
from DTOs.requestDtos.task import RequestAddNewTask, RequestEditTask, TaskDraggedInSameColumn, TaskDrgaggedInDifferentColumn
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
  print("position: ", [b.position for b in bucket.tasks], bucket_id)
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


def update_both_buckets(db: Session, new_Bucket_id: str, old_bucket_id: str):

  old_bucket = get_bucket_by_id(db, old_bucket_id)
  new_bucket = get_bucket_by_id(db, new_Bucket_id)

  for index, task in enumerate(sorted(old_bucket.tasks, key=lambda task: task.position)):
    task.position = index

  for index, task in enumerate(sorted(new_bucket.tasks, key=lambda task: task.position)):
    if(task.position == 1000000):
      task.position = 0
    else:
      task.position = index + 1

  db.commit()
  return db.query(Board).filter(Board.is_active == True).first()


def setTaskPosition(db: Session, draggedTask: TaskDraggedInSameColumn):

  bucket = get_bucket_by_id(db, draggedTask.bucketId)

  if bucket is not None and bucket.tasks is not None:
    for task in  bucket.tasks:
      filtered_ids  = list(filter(lambda x: x.id == task.id, draggedTask.tasksPosition))
      dragTask = filtered_ids[0]
      if dragTask is not None:
        task.position = dragTask.pos

  db.commit()
  return db.query(Board).filter(Board.is_active == True).first()


def setTaskPositions(db:Session, draggedTask: TaskDrgaggedInDifferentColumn):

  db_task = db.query(Task).filter(Task.id == draggedTask.taskId).first()
  db_task.bucket_id = draggedTask.finishTaskPosition.bucketId
  db.commit()
  db.refresh(db_task)

  setTaskPosition(db, draggedTask.startTaskPosition)
  setTaskPosition(db, draggedTask.finishTaskPosition)

  return db.query(Board).filter(Board.is_active == True).first()
      

