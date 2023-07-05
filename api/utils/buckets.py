from sqlalchemy.orm import Session
from DTOs.requestDtos.bucket import RequestCreateNewBucket

from db.models.board import Bucket, Board


def get_buckets(db: Session, skip: int = 0, limit: int = 50):

  return db.query(Bucket).offset(skip).limit(limit).all()



def get_bucket_by_id(db: Session, id: str) -> Bucket:
  
  return db.query(Bucket).filter(Bucket.id == id).first()

def get_bucket_by_name(db: Session, name: str) -> Bucket:
  
  return db.query(Bucket).filter(Bucket.name == name).first()


def create_bucket(db: Session, bucket: RequestCreateNewBucket) -> Bucket:
   
   position = 0
   board = db.query(Board).filter(Board.is_active == True)

   if board is not None:
     position = len(board.buckets)
   
   db_bucket = Bucket(name = bucket.name, board_id = bucket.boardId, position = position)

   db.add(db_bucket)
   db.commit()
   db.refresh(db_bucket)
   return db_bucket
  

def create_bucket_bulk(db: Session, buckets: list[Bucket]):

  for bucket in buckets:
    if isinstance(bucket, Bucket):
      db.add(bucket)
      db.commit()
      db.refresh(bucket)


def update_bucket_name(db: Session, id: str, name: str):

  bucket = get_bucket_by_id(db, id)
  bucket.name = name

  db.commit()
  db.refresh(bucket)
  return bucket


def delete_bucket(db: Session, id: str):

  bucket = db.query(Bucket).filter(Bucket.id == id).first()

  tasks = bucket.tasks
  if tasks is not None:
    for task in tasks:
      if task.subtasks is not None:
        for subtask in task.subtasks:
          # db.delete(subtask)
          pass

      db.delete(task)    

  db.delete(bucket)
  db.commit()

