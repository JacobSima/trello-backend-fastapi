from DTOs.reponseDtos.board import ResponseBoard
from db.models.board import Board
from api.utils.bucketResponse import get_bucket_response


def get_board_response(board: Board):

  buckets = [ get_bucket_response(bucket) for bucket in board.buckets ] if len(board.buckets) > 0 else []

  res_board = ResponseBoard(
    name = board.name,
    id = board.id,
    isActive = board.is_active,
    pos = board.position,
    columns = sorted(buckets, key=lambda bucket: bucket.pos)
  )
  return res_board


def build_boards_repsonse(boards: list[Board]):
  boards = [ get_board_response(board) for board in boards]
  return sorted(boards, key=lambda board: board.pos)