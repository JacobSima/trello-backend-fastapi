from DTOs.reponseDtos.subtask import ResponseSubTask
from db.models.board import SubTask


def get_subtask_reponse(subtask: SubTask) -> ResponseSubTask:
    
    res_subtask = ResponseSubTask(
      id = subtask.id,
      title = subtask.title,
      pos = subtask.position,
      taskId= subtask.task_id,
      isCompleted= subtask.isCompleted,
      existing = True
    )
  
    return res_subtask