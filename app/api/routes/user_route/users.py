from fastapi import APIRouter, HTTPException,Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import  JSONResponse
from app.api.schemas.schemas import TextInputUser
from sqlalchemy.orm import Session
from app.api.db.connection import get_session, token_verifier
from app.api.aplication.use_cases.user_cases import UseruseCases
from app.api.schemas.schemas import User
from app.api.db.models import UserEssaysModel


users_route = APIRouter()

@users_route.get("/kp", tags=["Users"])
async def userTextKeepAlive():
  return {"Server":"on"}

@users_route.post("/register", tags=["Users"])
async def user_register(user:User, db_session: Session = Depends(get_session)):
  uc = UseruseCases(db_session=db_session)
  uc.user_register(user)
  return JSONResponse(content="Sucesso ao criar usuário", status_code=201)


@users_route.post('/login', tags=["Users"])
def user_register(
    request_form_user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_session),
):
    uc = UseruseCases(db_session=db_session)
    user = User(
        username=request_form_user.username,
        password=request_form_user.password
    )

    auth_data = uc.user_login(user=user)
    return JSONResponse(
        content=auth_data,
        status_code=200
    )


@users_route.get('/test',tags=["Testes"])
def test_user_verify():
    return 'It works'


@users_route.get('/users/essays', tags=["Users"])
def list_user_essays(
    current_user = Depends(token_verifier),
    db_session: Session = Depends(get_session),
):
    try:
        essays = (
            db_session.query(UserEssaysModel)
            .filter_by(user_id=current_user.id)
            .order_by(UserEssaysModel.created_at.desc())
            .all()
        )

        response = []
        for e in essays:
            response.append({
                "id": e.id,
                "created_at": e.created_at,
                "input_text": e.input_text,
                "nota_total": e.nota_total,
                "stars": e.stars,
                "criterios": {
                    "norma":       {"nota": e.c1_nota, "obs": e.c1_obs, "stars": e.c1_stars},
                    "repertorio":  {"nota": e.c2_nota, "obs": e.c2_obs, "stars": e.c2_stars},
                    "coerencia":   {"nota": e.c3_nota, "obs": e.c3_obs, "stars": e.c3_stars},
                    "coesao":      {"nota": e.c4_nota, "obs": e.c4_obs, "stars": e.c4_stars},
                    "intervencao": {"nota": e.c5_nota, "obs": e.c5_obs, "stars": e.c5_stars},
                }
            })

        return response
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
