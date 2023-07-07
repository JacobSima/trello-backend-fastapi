from pydantic import BaseModel


class RequestDeleteBucket(BaseModel):
  id: str


class RequestCreateNewBucket(BaseModel):
  name: str
  boardId: str | None

class RequestDraggedBucket(BaseModel):
  sourceIndex: int
  destinationIndex: int