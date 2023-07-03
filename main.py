from fastapi import FastAPI

from api import boards, buckets, tasks, subtasks


app = FastAPI(
  title="Opus 1 Kanban Board",
  description="Board Management of tasks of different scenarios",
  version="0.0.1",
  contact={
    "name": "Jacob",
    "email": "jazzy@opus1.io",
  },
  license_info={
    "name": "MIT",
  }
)


# Register all Routes
app.include_router(boards.router)
app.include_router(buckets.router)
app.include_router(tasks.router)
app.include_router(subtasks.router)

