
from fastapi import APIRouter, HTTPException, Body, Depends
from app.api.schemas.schemas import TextInputUser
from app.api.aplication.use_cases.user_cases import UseruseCases
from app.api.services.openai_client import TextAnalyzer
from app.api.db.connection import token_verifier
from sqlalchemy.orm import Session
from app.api.db.connection import get_session
from app.api.db.models import UserModel  

analysis_route = APIRouter()
text_analysis = TextAnalyzer()

@analysis_route.get("/analysis/text/kp", tags=["Analysis"])
async def analysisTextKeepAlive():
    return {"Server":"on"}

@analysis_route.post("/analysis/text", tags=["Analysis"])
async def analysisText(
    payload: TextInputUser,
    current_user = Depends(token_verifier),  
    db_session: Session = Depends(get_session)
):
    user_case = UseruseCases(db_session=db_session)
    try:
        result = text_analysis.analyze(payload.text)
        saved = user_case.save_essays(
            user_id=current_user.id,    
            analysis_result=result,
            original_text=payload.text
        )
        # Devolva o resultado + ID salvo para poder consultar depois
        return {"essay_id": saved.id, **result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
