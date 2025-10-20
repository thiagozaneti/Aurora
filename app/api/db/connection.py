import os
from fastapi import Depends
from dotenv import load_dotenv
from sqlalchemy import create_engine
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker
from app.api.aplication.use_cases.user_cases import UseruseCases

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_engine(url=DB_URL,pool_pre_ping=True)
Session = sessionmaker(bind = engine)
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')


def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def token_verifier(
    db_session: Session = Depends(get_session),
    token = Depends(oauth_scheme)
):
    uc = UseruseCases(db_session=db_session)
    uc.verify_token(access_token=token)
