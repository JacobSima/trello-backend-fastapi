
from DTOs.reponseDtos.board import ResponseBoard
from db.models.board import Board
from api.utils.bucketResponse import get_bucket_response


def get_board_response(board: Board):

  res_board = ResponseBoard(
    name = board.name,
    id = board.id,
    isActive = board.is_active,
    pos = board.position,
    columns = [ get_bucket_response(bucket) for bucket in board.buckets ] if len(board.buckets) > 0 else []
  )
  
  return res_board


def build_boards_repsonse(boards: list[Board]):
  return [ get_board_response(board) for board in boards]