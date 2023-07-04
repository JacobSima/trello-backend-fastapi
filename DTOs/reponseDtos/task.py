from pydantic import BaseModel, Field
from typing import List, Any


class ResponseDeleteTask(BaseModel):
  id: str


class ResponseTask(BaseModel):
  id: str
  title: str
  description: str
  status: str
  pos: int
  bucketId: str
  subtasks: List[Any]
  existing: bool = Field(default=True)