from fastapi import FastAPI
import uvicorn
from app.api.routes.analysis_route.analysis import analysis_route

app = FastAPI()
app.include_router(analysis_route,prefix="/api/v1")


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=4)

