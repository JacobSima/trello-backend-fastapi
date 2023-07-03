import fastapi

router = fastapi.APIRouter()

subtasks = []

@router.get("/api/subtasks")
async def getAllSubTasks():
  return {"subtasks": "subtasks"}