from pydantic import BaseModel, Field


# Add task Modal data
class RequestAddNewTask(BaseModel):
    title: str
    description: str | None
    subtasks: list[str]
    bucketId: str

class RequestEditSubTasks(BaseModel):
    id: str | None
    title: str
    isCompleted: bool = Field(default=False)   # if deleted in front-end => isCompleted = True
    taskId: str | None
    deleted: bool = Field(default=False)
    new: bool = Field(default=False)
    updated: bool = Field(default=False)

class RequestEditTask(BaseModel):
    id: str
    title: str | None
    description: str | None
    status: str | None
    bucketId: str
    subtasks: list[RequestEditSubTasks]
 