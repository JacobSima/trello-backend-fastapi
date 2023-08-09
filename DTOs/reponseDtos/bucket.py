from pydantic import BaseModel, Field
from typing import List
from DTOs.reponseDtos.task import ResponseTask


class ResponseDeleteBucket(BaseModel):
  id: str


class ResponseBucket(BaseModel):
  name: str
  id: str
  boardId: str
  pos: int
  existing: bool = Field(default=True)
  tasks: List[ResponseTask]