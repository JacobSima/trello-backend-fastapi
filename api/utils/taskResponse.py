from api.utils.subTaskResponse import get_subtask_reponse
from db.models.board import Task
from DTOs.reponseDtos.task import ResponseTask


def get_task_reponse(task: Task) -> ResponseTask:

  subtasks = [ get_subtask_reponse(subtask) for subtask in task.subtasks if subtask.isCompleted == False] if len(task.subtasks) > 0 else []
    
  res_task = ResponseTask(
    id = task.id,
    title = task.title,
    description= task.description,
    status= task.bucket.name,
    pos = task.position,
    subtasks = sorted(subtasks, key=lambda subtask: subtask.pos),
    bucketId= task.bucket_id,
    existing = True
  )

  return res_task