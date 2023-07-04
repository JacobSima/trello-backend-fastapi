from DTOs.reponseDtos.bucket import ResponseBucket
from db.models.board import Bucket
from api.utils.taskResponse import get_task_reponse


def get_bucket_response(bucket: Bucket):
    
    res_bucket = ResponseBucket(
      id = bucket.id,
      name = bucket.name,
      boardId = bucket.board_id,
      pos = bucket.position,
      tasks = [ get_task_reponse(task) for task in bucket.tasks ] if len(bucket.tasks) > 0 else []
    )
  
    return res_bucket


def get_buckets_reponse(buckets: list[Bucket]):
    return [ get_bucket_response(bucket) for bucket in buckets]
