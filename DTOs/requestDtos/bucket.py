from pydantic import BaseModel


class RequestDeleteBucket(BaseModel):
  id: str


class RequestCreateNewBucket(BaseModel):
  name: str

class RequestDraggedBucket(BaseModel):
  sourceIndex: int
  sourceId: str
  destinationIndex: int
  destinationId: str