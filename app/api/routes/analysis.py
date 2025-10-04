from fastapi import APIRouter, HTTPException,Body
from api.models.user_input_models import TextInputUser
from api.services.openai_client import TextAnalyzer
import logging

analysis_route = APIRouter()
text_analysis = TextAnalyzer()
logger = logging.getLogger(__name__)

@analysis_route.get("/analysis/text/kp")
async def analysisTextKeepAlive():
  return {"Server":"on"}

@analysis_route.post("/analysis/text", tags=["Analysis"])
async def analysisText(payload:TextInputUser):
  try:
    result = text_analysis.analyze(payload.text)
    logger.info("Endpoint acessado")
    return result
    
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
