from sqlalchemy.orm import Session
from DTOs.requestDtos.task import RequestAddNewTask, RequestEditSubTasks, RequestEditTask
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


def  save__subtasks(db: Session, subtasks: list[RequestEditSubTasks]):

  for subtask in subtasks:
    db_subtask = db.query(SubTask).filter(SubTask.id == subtask.id).first()
    db_subtask.isCompleted = subtask.isCompleted if subtask.isCompleted is not None else db_subtask.isCompleted
    db_subtask.title = subtask.title if subtask.title is not None else db_subtask.title
    db_subtask.position = subtask.position if subtask.position is not None else db_subtask.position
  
  db.commit()