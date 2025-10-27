from fastapi import APIRouter, HTTPException,Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import  JSONResponse
from app.api.schemas.schemas import TextInputUser
from sqlalchemy.orm import Session
from app.api.db.connection import get_session
from app.api.aplication.use_cases.user_cases import UseruseCases
from app.api.schemas.schemas import User


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
