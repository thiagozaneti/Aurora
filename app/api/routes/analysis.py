from fastapi import APIRouter, HTTPException,Body
from models.user_input_models import TextInputUser
from services.openai_client import TextAnalyzer

analysis_route = APIRouter()
text_analysis = TextAnalyzer()

@analysis_route.get("/analysis/text/kp")
async def analysisTextKeepAlive():
  return {"Server":"on"}

@analysis_route.post("/analysis/text", tags=["Analysis"])
async def analysisText(payload:TextInputUser):
  try:
    result = text_analysis.analyze(payload.text)
    return result
    
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
