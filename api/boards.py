import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from uuid import uuid4, UUID

from DTOs.requestDtos.board import RequestCreateNewBoard, RequestEditBoardNameOnly, RequestEditBoard
from api.utils.boards import get_boards, create_board, update_active_board_status, update_board_name, get_board
from api.utils.buckets import create_bucket_bulk, update_bucket_name, delete_bucket, update_bucket_position
from db.db_setup import get_db
from db.models.board import Bucket
from api.utils.boardResponse import build_boards_repsonse, get_board_response

router = fastapi.APIRouter()


@router.get("/api/boards")
async def getAllBoards(skip: int = 0, limit : int = 100, db: Session = Depends(get_db)):

  boards = get_boards(db, skip, limit)

  if boards is not None:
    boards_response = build_boards_repsonse(boards)
    return {"boards": boards_response}
  
  return {"boards": {}}



@router.get("/api/boards/{board_id}")
async def getBoard(board_id: str, db: Session = Depends(get_db)):

  board = get_board(db, board_id)

  if board is not None:
    board_response = get_board_response(board)
    return {"boards": board_response}
  
  return {"board": {}} # Error



@router.post("/api/boards", status_code=201)
async def createBoard(board: RequestCreateNewBoard, db: Session = Depends(get_db)):

  created_board = create_board(db, board)

  if created_board:

    buckets = [ Bucket(name = name, position = index, board_id = created_board.id) for index, name in enumerate(board.buckets)]
    create_bucket_bulk(db, created_board.id, buckets)
    update_active_board_status(db, created_board.id)

    board_response = get_board_response(created_board)
    return {"board": board_response}
  
  return {"board": "created"}  # Error



@router.put("/api/boards/updatenameonly")
async def updateNameOnly(board: RequestEditBoardNameOnly, db: Session = Depends(get_db)):
  
  board = update_board_name(db, board.id, board.name)

  board_response = get_board_response(board)
  return {"board": board_response}



@router.put("/api/boards/editboard")
async def editBoard(board: RequestEditBoard, db: Session = Depends(get_db)):

  #  get delete 
  deleted_buckets = [ board for board in board.buckets if board.deleted == True ]
  updated_buckets = [ board for board in board.buckets if board.updated == True ]
  new_buckets = [ board for board in board.buckets if board.new == True ]

  if board.nameChanged:
    update_board_name(db, board.id, board.name)


  if len(updated_buckets) > 0 : 
    for bucket in updated_buckets:
      update_bucket_name(db, bucket.id, bucket.name)

  if len(deleted_buckets) > 0 :
    for bucket in deleted_buckets:
      delete_bucket(db, bucket.id)
    update_bucket_position(db, board.id)


  if len(new_buckets) > 0 :
    buckets = [ Bucket(name = item.name, position = index, board_id = board.id) for index, item in enumerate(new_buckets)]
    create_bucket_bulk(db, buckets)
    update_bucket_position(db, board.id)
  
    
  board_updated = get_board(db, board.id)
  board_response = get_board_response(board_updated)
  return {"board": board_response}




# @router.delete("/api/boards/{boardId}")
# async def deleteBoard(boardId: UUID):
#   delete_board_by_id(boardId)
#   return "deleted"