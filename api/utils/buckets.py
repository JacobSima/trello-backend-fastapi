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
   board = db.query(Board).filter(Board.is_active == True).first()

   if board is not None and len(board.buckets) > 0:
     position = max(tuple([ bucket.position for bucket in board.buckets])) + 1
   
   db_bucket = Bucket(name = bucket.name, board_id = board.id, position = position)

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
  
  if bucket.tasks is not None:
    for task in bucket.tasks:
      if task.subtasks is not None:
        for subtask in task.subtasks:
          db.delete(subtask)
          pass

      db.delete(task)    

  db.delete(bucket)
  db.commit()


def update_bucket_position(db: Session):
  board = db.query(Board).filter(Board.is_active == True).first()

  if board.buckets is not None:
    for index, bucket in enumerate(sorted(board.buckets, key= lambda bucket: bucket.position) ):
      bucket.position = index
    db.commit()
  return board


