from pydantic import BaseModel, Field


# Add New baord modal data
class RequestCreateNewBoard(BaseModel):
  name : str
  buckets: list[str] 



# Edit Board Modal data, if name only changed
class RequestEditBoardNameOnly(BaseModel):
  name: str
  id:str


# Edit Board columns data
class RequestBoardEditedBucket(BaseModel):
    name: str
    id:str | None
    deleted: bool = Field(default=False)   # if deleted
    updated: bool = Field(default=False)  # check name(with reducer), if changed
    new: bool = Field(default=False) # newly created bucket



# Board to Edit
class RequestEditBoard(BaseModel):
    name: str
    id:str
    nameChanged: bool = Field(default=False)
    buckets: list[RequestBoardEditedBucket] = []





