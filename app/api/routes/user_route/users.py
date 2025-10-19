from fastapi import APIRouter, HTTPException,Body
from app.api.schemas.schemas import TextInputUser

users_route = APIRouter()

@users_route.get("/users/kp", tags=["Users"])
async def analysisTextKeepAlive():
  return {"Server":"on"}
