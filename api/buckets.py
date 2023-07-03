import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from DTOs.requestDtos.bucket import RequestCreateNewBucket
from db.db_setup import get_db
from api.utils.buckets import get_buckets, create_bucket, get_bucket_by_id
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
  db_bucket =  get_bucket_response(bucket)
  
  return {"bucket": db_bucket}