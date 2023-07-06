import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from DTOs.requestDtos.bucket import RequestCreateNewBucket
from api.utils.boardResponse import get_board_response
from api.utils.boards import get_active_Board, get_board
from db.db_setup import get_db
from api.utils.buckets import delete_bucket, get_buckets, create_bucket, get_bucket_by_id, update_bucket_position
from api.utils.bucketResponse import get_buckets_reponse, get_bucket_response


router = fastapi.APIRouter()


@router.get("/api/buckets")
async def getAllBucktes(skip: int = 0, limit : int = 100, db: Session = Depends(get_db)):

  buckets = get_buckets(db, skip, limit)
  db_buckets =  get_buckets_reponse(buckets)
  
  return {"buckets": db_buckets}


@router.get("/api/buckets/{bucket_id}")
async def getBucket(bucket_id: str, db: Session = Depends(get_db)):
  
  bucket = get_bucket_by_id(db, id = bucket_id)
  db_bucket =  get_bucket_response(bucket)
  
  return {"buckets": db_bucket}


@router.post("/api/buckets")
async def getBucket(bucket: RequestCreateNewBucket ,db: Session = Depends(get_db)):

  bucket = create_bucket(db, bucket)
  board = update_bucket_position(db)

  board_response = get_board_response(board)
  return {"board": board_response}


@router.delete("/api/bucket/{bucket_id}")
async def deleteBucket(bucket_id: str, db: Session = Depends(get_db)):

  delete_bucket(db, bucket_id)
  board = update_bucket_position(db)
  board_response = get_board_response(board)
  return {"board": board_response}