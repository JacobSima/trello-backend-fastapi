from pydantic import BaseModel, Field


# Add New baord modal data
class RequestCreateNewBoard(BaseModel):
  name : str
  isActive: bool = Field(default=False)
  buckets: list[str] 



# Edit Board Modal data, if name only changed
class RequestEditBoardNameOnly(BaseModel):
  name: str
  id:str


# Edit Board columns data
class RequestBoardEditedBucket(BaseModel):
    name: str
    id:str
    deleted: bool = Field(default=False)   # if deleted
    updated: bool = Field(default=False)  # check name(with reducer), if changed
    new: bool = Field(default=False) # newly created bucket



# Board to Edit
class RequestEditBoard(BaseModel):
    name: str
    id:str
    nameChanged: bool = Field(default=False)
    buckets: list[RequestBoardEditedBucket] = []



# Request to delete Board
class RequestDeleteBoard(BaseModel):
  boardId:str





