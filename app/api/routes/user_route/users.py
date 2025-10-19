from fastapi import APIRouter, HTTPException,Body
from api.models.user_input_models import TextInputUser

users_route = APIRouter()

@users_route.get("/users/kp", tags=["Users"])
async def analysisTextKeepAlive():
  return {"Server":"on"}
