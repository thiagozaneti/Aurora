# app/api/aplication/use_cases/user_cases.py
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from app.api.db.models import UserModel, UserEssaysModel
from app.api.schemas.schemas import User
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from decouple import config
from typing import Dict, Any

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_context = CryptContext(schemes=['sha256_crypt'])

def _get_criterio(analysis: Dict[str, Any], key: str) -> Dict[str, Any]:
    c = (analysis.get("criterios") or {}).get(key) or {}
    return {
        "nota": int(c.get("nota") or 0),
        "obs":  str(c.get("observacoes") or c.get("obs") or ""),
        "stars": int(c.get("stars") or 0)
    }

class UseruseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_essay(self, user_id: int, input_text: str, result: dict) -> UserEssaysModel:
        def _get(comp: str, field: str, alt: str = None, default=None):
            c = (result.get("criterios") or {}).get(comp) or {}
            v = c.get(field)
            if v is None and alt is not None:
                v = c.get(alt)
            return default if v is None else v

        # C1..C5
        c1_nota  = int(_get("norma",       "nota",           default=0))
        c1_obs   = str(_get("norma",       "comentarioC1",   alt="comentario", default=""))
        c1_stars = int(_get("norma",       "starsC1",        alt="stars",      default=0))

        c2_nota  = int(_get("repertorio",  "nota",           default=0))
        c2_obs   = str(_get("repertorio",  "comentarioC2",   alt="comentario", default=""))
        c2_stars = int(_get("repertorio",  "starsC2",        alt="stars",      default=0))

        c3_nota  = int(_get("coerencia",   "nota",           default=0))
        c3_obs   = str(_get("coerencia",   "comentarioC3",   alt="comentario", default=""))
        c3_stars = int(_get("coerencia",   "starsC3",        alt="stars",      default=0))

        c4_nota  = int(_get("coesao",      "nota",           default=0))
        c4_obs   = str(_get("coesao",      "comentarioC4",   alt="comentario", default=""))
        c4_stars = int(_get("coesao",      "starsC4",        alt="stars",      default=0))

        c5_nota  = int(_get("intervencao", "nota",           default=0))
        c5_obs   = str(_get("intervencao", "comentarioC5",   alt="comentario", default=""))
        c5_stars = int(_get("intervencao", "starsC5",        alt="stars",      default=0))

        # nota_total do modelo
        nota_total = int(result.get("nota_total") or (c1_nota + c2_nota + c3_nota + c4_nota + c5_nota))

        stars_total = c1_stars+ c2_stars+ c3_stars+ c4_stars+ c5_stars

        row = UserEssaysModel(
            user_id=user_id,
            input_text=input_text or "",

            c1_nota=c1_nota, c1_obs=c1_obs, c1_stars=c1_stars,
            c2_nota=c2_nota, c2_obs=c2_obs, c2_stars=c2_stars,
            c3_nota=c3_nota, c3_obs=c3_obs, c3_stars=c3_stars,
            c4_nota=c4_nota, c4_obs=c4_obs, c4_stars=c4_stars,
            c5_nota=c5_nota, c5_obs=c5_obs, c5_stars=c5_stars,

            stars=stars_total,
            nota_total=nota_total,
        )

        self.db_session.add(row)
        self.db_session.commit()
        self.db_session.refresh(row)
        return row

    # ===== seus métodos existentes abaixo =====
    def user_register(self, user:User):
        user_model = UserModel(
            username = user.username,
            password = crypt_context.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(status_code=400, detail="usuário já existente")

    def user_login(self, user: User, expires_in: int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first()
        if user_on_db is None or not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(status_code=401, detail='Invalid username or password')

        exp = datetime.utcnow() + timedelta(minutes=expires_in)
        payload = {'sub': user.username, 'exp': exp}
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {'access_token': access_token, 'exp': exp.isoformat()}

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail='Invalid access token')

        user_on_db = self.db_session.query(UserModel).filter_by(username=data['sub']).first()
        if user_on_db is None:
            raise HTTPException(status_code=401, detail='Invalid access token')
        return user_on_db
