from sqlalchemy.orm import Session
from DTOs.requestDtos.task import RequestAddNewTask
from api.utils.buckets import get_bucket_by_id
from db.models.board import Bucket, Task, SubTask


def create_subTask_bulk(db: Session, subtasks: list[str], task_id: str):
  
  for index, subtask in enumerate(subtasks):
    db_subtask = SubTask(
      title = subtask,
      position = index,
      isCompleted = False,
      task_id = task_id
    )

    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
