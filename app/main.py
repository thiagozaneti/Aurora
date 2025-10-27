from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.analysis_route.analysis import analysis_route
from app.api.routes.user_route.users import users_route
from app.api.db.base import Base
from app.api.db.connection import engine
from app.api.db import models  # ensure models are registered

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
app.include_router(analysis_route,prefix="/api/v1")
app.include_router(users_route,prefix="/api/v1")


if __name__ == "__main__":
  uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, workers=4)

