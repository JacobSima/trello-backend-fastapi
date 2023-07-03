from DTOs.reponseDtos.bucket import ResponseBucket
from db.models.board import Bucket


def get_bucket_response(bucket: Bucket):
    
    res_bucket = ResponseBucket(
      id = bucket.id,
      name = bucket.name,
      boardId = bucket.board_id,
      pos = bucket.position,
      tasks = []
    )
  
    return res_bucket


def get_buckets_reponse(buckets: list[Bucket]):
    return [ get_bucket_response(bucket) for bucket in buckets]
