import fastapi

router = fastapi.APIRouter()

tasks = []

@router.get("/api/tasks")
async def getAllTasks():
  return {"tasks": "tasks"}
