from pydantic import BaseModel, Field


# Add task Modal data
class RequestAddNewTask(BaseModel):
    title: str
    description: str | None
    subtasks: list[str]
    bucketId: str

class RequestEditSubTasks(BaseModel):
    id: str
    title: str
    isCompleted: bool = Field(default=False)   # if deleted in front-end => isCompleted = True
    taskId: str

class RequestEditTask(BaseModel):
    id: str
    title: str
    description: str | None
    status: str
    bucketId: str
    subtasks: list[RequestEditSubTasks]


    