from pydantic import BaseModel, Field

from DTOs.reponseDtos.bucket import ResponseBucket

class ResponseBoard(BaseModel):
    id: str
    name: str
    pos: int
    isActive: bool = Field(default=False)
    existing: bool = Field(default=True)
    columns: list[ResponseBucket]
