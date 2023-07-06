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


def saveCompletedSubtasks(db: Session, subtask: RequestEditSubTasks):

  db_subtask = db.query(SubTask).filter(SubTask.id == subtask.id).first()

  if db_subtask:
    db_subtask.isCompleted = True
    db.commit()
    db.refresh(db_subtask)


def  updateSubtask(db: Session, subtask: RequestEditSubTasks):

  db_subtask = db.query(SubTask).filter(SubTask.id == subtask.id).first()
  
  db_subtask.title = subtask.title if subtask.title is not None else db_subtask.title

  db.commit()
  db.refresh(db_subtask)


def  saveNewSubtask(db: Session, subtask: RequestEditSubTasks, id: str):
  task = db.query(Task).filter(Task.id == id).first()
  position = len(task.subtasks) if task.subtasks is not None else 0

  db_subtask = SubTask(
      title = subtask.title,
      position = position,
      isCompleted = False,
      task_id = id
    )

  db.add(db_subtask)
  db.commit()
  db.refresh(db_subtask)