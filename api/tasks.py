import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from DTOs.requestDtos.task import RequestAddNewTask, RequestEditTask
from api.utils.boardResponse import get_board_response
from api.utils.bucketResponse import get_bucket_response
from api.utils.buckets import get_bucket_by_id, get_bucket_by_name

from api.utils.tasks import get_tasks, get_task, create_task, update_task, update_both_buckets, update_task_bucteks, update_task_position
from api.utils.taskResponse import get_task_reponse
from api.utils.subtasks import create_subTask_bulk, saveCompletedSubtasks, saveNewSubtask, updateSubtask
from db.db_setup import get_db

router = fastapi.APIRouter()



@router.get("/api/tasks")
async def getAllTasks(skip: int = 0, limit : int = 100, db: Session = Depends(get_db)):

  tasks =  get_tasks(db, skip, limit)

  return {"tasks": tasks}



@router.get("/api/tasks/{task_id}")
async def getTask(task_id: str, db: Session = Depends(get_db)):

  tasks =  get_task(db, task_id)

  return {"tasks": tasks}



@router.post("/api/tasks")
async def createTask(task: RequestAddNewTask , db: Session = Depends(get_db)):

  task_created =  create_task(db, task.bucketId, task)

  create_subTask_bulk(db, task.subtasks, task_created.id)

  updated_task = get_task(db, task_created.id)
  
  bucket = update_task_position(db, updated_task.bucket_id)

  bucket_response = get_bucket_response(bucket)

  return {"bucket": bucket_response}


@router.put("/api/tasks/edittasksamebucket")
async def editTak(task: RequestEditTask, db: Session = Depends(get_db)):
  
 
  for subtask in [sub for sub in task.subtasks if sub.deleted == True]:
    saveCompletedSubtasks(db, subtask)

  for subtask in [sub for sub in task.subtasks if sub.updated == True]:
    updateSubtask(db, subtask)

  for subtask in [sub for sub in task.subtasks if sub.new == True]:
    saveNewSubtask(db, subtask, task.id)
  
  updatedTask = update_task(db, task)

  bucket = update_task_position(db, updatedTask.bucket_id)

  bucket_response = get_bucket_response(bucket)

  return {"bucket": bucket_response}


@router.put("/api/tasks/edittaskchangebucket")
async def editTak(task: RequestEditTask, db: Session = Depends(get_db)):
  
  for subtask in [sub for sub in task.subtasks if sub.deleted == True]:
    saveCompletedSubtasks(db, subtask)

  for subtask in [sub for sub in task.subtasks if sub.updated == True]:
    updateSubtask(db, subtask)

  for subtask in [sub for sub in task.subtasks if sub.new == True]:
    saveNewSubtask(db, subtask, task.id)
  
  updatedTask = update_task_bucteks(db, task)


  board = update_both_buckets(db, updatedTask.bucket_id, task.bucketId, updatedTask.id)

  board_response = get_board_response(board )

  return {"board": board_response}



  
  
  


