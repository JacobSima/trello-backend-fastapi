from sqlalchemy.orm import Session
from DTOs.requestDtos.board import RequestCreateNewBoard

from db.models.board import Board


def get_boards(db: Session, skip: int = 0, limit: int = 50) -> list[Board]:

  return db.query(Board).offset(skip).limit(limit).all()


def get_board(db: Session, id: str) -> Board:

  return db.query(Board).filter(Board.id == id).first()



def get_board_by_id(db: Session, id: str) -> Board:
  
  return db.query(Board).filter(Board.id == id).first()


def update_active_board_status(db: Session, id: str) -> None:

  boards = db.query(Board).all()
  for board in boards:
    if board.id == id:
      board.is_active = True
    else:
      board.is_active = False

  db.commit()


def create_board(db: Session, board: RequestCreateNewBoard) -> Board:

  db_board = Board(name = board.name,is_active = True,position = len(get_boards(db)))

  db.add(db_board)
  db.commit()
  db.refresh(db_board)

  return db_board


def update_board_name(db: Session, id: str, name: str) -> Board:

  board = get_board_by_id(db, id)
  board.name = name

  db.commit()
  db.refresh(board)
  
  return board