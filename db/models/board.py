from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp
from .common import generate_uuid


class Board(Timestamp, Base):
  __tablename__ = "boards"

  id = Column(String, primary_key=True, default=generate_uuid, unique=True, nullable=False)
  name = Column(String(100), nullable=False)
  is_active = Column(Boolean, default=False)
  position = Column(Integer, nullable=False)

  buckets =  relationship("Bucket", back_populates="board")


class Bucket(Timestamp, Base):
  __tablename__ = "bucktes"

  id = Column(String, primary_key=True, default=generate_uuid, unique=True, nullable=False)
  name = Column(String(100), nullable=False)
  position = Column(Integer, nullable=False)
  board_id = Column(String, ForeignKey("boards.id"), nullable=False)

  board =  relationship("Board", back_populates="buckets")    # Board.buckets => from Board
