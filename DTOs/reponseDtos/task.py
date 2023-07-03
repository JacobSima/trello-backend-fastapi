from pydantic import BaseModel, Field
from typing import List, Any


class ResponseDeleteTask(BaseModel):
  id: str


class ResponseTask(BaseModel):
  id: str
  title: str
  description: str
  status: str
  position: int
  subtasks: List[Any]
  existing: bool = Field(default=True)