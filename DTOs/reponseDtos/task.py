from pydantic import BaseModel, Field
from typing import List, Any
from DTOs.reponseDtos.subtask import ResponseSubTask


class ResponseDeleteTask(BaseModel):
  id: str


class ResponseTask(BaseModel):
  id: str
  title: str
  description: str
  status: str
  pos: int
  bucketId: str
  subtasks: List[ResponseSubTask]
  existing: bool = Field(default=True)