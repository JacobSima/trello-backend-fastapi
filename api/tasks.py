import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from DTOs.requestDtos.task import RequestAddNewTask, RequestEditTask

from api.utils.tasks import get_tasks, get_task, create_task, update_task_position
from api.utils.taskResponse import get_task_reponse
from api.utils.subtasks import create_subTask_bulk
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
  
  update_task_position(db, task.bucketId)

  updated_task = get_task(db, task_created.id)
  
  task_reponse = get_task_reponse(updated_task)

  return {"task": task_reponse}


@router.put("/api/tasks/edittask")
async def editTak(task: RequestEditTask, db: Session = Depends(get_db)):
  
  pass


