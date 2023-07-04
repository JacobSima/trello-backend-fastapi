from pydantic import BaseModel, Field
from typing import List, Any


class ResponseDeleteTask(BaseModel):
  id: str


class ResponseSubTask(BaseModel):
  id: str
  title: str
  pos: int
  taskId: str
  isCompleted: bool = Field(default=False)
  existing: bool = Field(default=True)