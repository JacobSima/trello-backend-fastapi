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
  tasks = relationship("Task", back_populates="bucket")


class Task(Timestamp, Base):
  __tablename__ = "tasks"

  id = Column(String, primary_key=True, default=generate_uuid, unique=True, nullable=False)
  title = Column(String(200), nullable=False)
  description = Column(Text, nullable=True)
  status = Column(String(20), nullable=False)
  position = Column(Integer, nullable=False)
  bucket_id = Column(String, ForeignKey("bucktes.id"), nullable=False)

  bucket = relationship("Bucket", back_populates="tasks")
  subtasks = relationship("SubTask", back_populates="task")


class SubTask(Timestamp, Base):
  __tablename__ = "subtasks"

  id = Column(String, primary_key=True, default=generate_uuid, unique=True, nullable=False)
  title = Column(String(200), nullable=False)
  position = Column(Integer, nullable=False)
  isCompleted = Column(Boolean, default=False)
  task_id = Column(String, ForeignKey("tasks.id"), nullable=False)

  task = relationship("Task", back_populates="subtasks")





