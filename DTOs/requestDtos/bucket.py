from pydantic import BaseModel


class RequestDeleteBucket(BaseModel):
  id: str


class RequestCreateNewBucket(BaseModel):
  name: str
  boardId: str