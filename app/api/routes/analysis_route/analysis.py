# app/api/routes/analysis.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api.schemas.schemas import TextInputUser
from app.api.aplication.use_cases.user_cases import UseruseCases
from app.api.services.openai_client import TextAnalyzer
from app.api.db.connection import token_verifier, get_session

analysis_route = APIRouter()
text_analysis = TextAnalyzer()

@analysis_route.get("/analysis/text/kp", tags=["Analysis"])
async def analysisTextKeepAlive():
    return {"Server": "on"}

@analysis_route.post("/analysis/text", tags=["Analysis"])
async def analysisText(
    payload: TextInputUser,
    current_user = Depends(token_verifier),         
    db_session: Session = Depends(get_session),
):
    try:
        if not payload.text or not payload.text.strip():
            raise HTTPException(status_code=422, detail="Campo 'text' vazio.")

        result = text_analysis.analyze(payload.text)

        user_case = UseruseCases(db_session=db_session)
        saved = user_case.save_essay(
            user_id=current_user.id,                 
            input_text=payload.text.strip(),
            result=result
        )

        return {
            "id": saved.id,
            "created_at": saved.created_at,
            "nota_total": saved.nota_total,
            "stars": saved.stars,
            "criterios": result.get("criterios", {}),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
