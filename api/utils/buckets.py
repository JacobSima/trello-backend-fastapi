from sqlalchemy.orm import Session
from DTOs.requestDtos.bucket import RequestCreateNewBucket
from DTOs.requestDtos.board import RequestBoardEditedBucket, RequestCreateNewBoard

from db.models.board import Bucket, Board
from api.utils.boards import get_board_by_id


def get_buckets(db: Session, skip: int = 0, limit: int = 50):

  return db.query(Bucket).offset(skip).limit(limit).all()



def get_bucket_by_id(db: Session, id: str) -> Bucket:
  
  return db.query(Bucket).filter(Bucket.id == id).first()


def create_bucket(db: Session, bucket: RequestCreateNewBucket) -> Bucket:
   
   position = 0
   board = get_board_by_id(db, bucket.boardId)

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


def update_bucket_position(db: Session, id: str):
  buckets = db.query(Bucket).all()

  for index, bucket in enumerate(buckets):
    bucket.position = index

  db.commit()


def delete_bucket(db: Session, id: str):

  board = db.query(Bucket).filter(Bucket.id == id).first()
  
  # TODO: also remove tasks linked to this bucket
  db.delete(board)
  db.commit()

