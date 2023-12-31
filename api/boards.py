import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends

from DTOs.requestDtos.board import RequestCreateNewBoard, RequestEditBoard
from api.utils.boards import delete_board_by_id, get_boards, create_board, update_active_board_status, update_board_name, get_board, update_board_active, set_active_board
from api.utils.buckets import create_bucket_bulk, update_bucket_name, delete_bucket, update_bucket_position
from db.db_setup import get_db
from db.models.board import Bucket
from api.utils.boardResponse import build_boards_repsonse, get_board_response

router = fastapi.APIRouter()

@router.get("/")
async def root():
  return {"message": "Welcome to Opus1.io Mini Trello"}

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

@router.get("/api/boards/updateactiveboard/{id}")
async def updateActiveBoard(id: str, db: Session = Depends(get_db)):
  update_board_active(db, id)
  return {"success": True}


@router.post("/api/boards", status_code=201)
async def createBoard(board: RequestCreateNewBoard, db: Session = Depends(get_db)):

  created_board = create_board(db, board)

  if created_board:

    buckets = [ Bucket(name = name, position = index, board_id = created_board.id) for index, name in enumerate(board.buckets)]
    create_bucket_bulk(db, buckets)
    board_updated = update_active_board_status(db, created_board.id)

    board_response = get_board_response(board_updated)
    return {"board": board_response}
  
  return {"board": "created"}  # Error



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
  
  if len(new_buckets) > 0 :
    existingBoard = get_board(db, board.id)
    boardLen = max(tuple([bucket.position for bucket in existingBoard.buckets])) + 1 if len(existingBoard.buckets) > 0 else 1

    buckets = [ Bucket(name = item.name, position = boardLen + index, board_id = board.id) for index, item in enumerate(new_buckets)]
    create_bucket_bulk(db, buckets)

  if len(deleted_buckets) > 0 :
    for bucket in deleted_buckets:
      delete_bucket(db, bucket.id)

  update_bucket_position(db)
  board_updated = get_board(db, board.id)
  board_response = get_board_response(board_updated)
  return {"board": board_response}


@router.delete("/api/boards/{board_id}")
async def deleteBoard(board_id: str, db: Session = Depends(get_db)):

  delete_board_by_id(db, board_id)
  set_active_board(db)
  return {"success": True}
