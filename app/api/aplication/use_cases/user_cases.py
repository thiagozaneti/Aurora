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

    def save_essays(self, *, user_id: int, analysis_result: Dict[str, Any], original_text: str) -> UserEssaysModel:
        try:
            c1 = _get_criterio(analysis_result, "coerencia")
            c2 = _get_criterio(analysis_result, "coesao")
            c3 = _get_criterio(analysis_result, "norma")
            c4 = _get_criterio(analysis_result, "repertorio")
            c5 = _get_criterio(analysis_result, "intervencao")

            nota_total = int(analysis_result.get("nota_total") or 0)

            essay = UserEssaysModel(
                user_id=user_id,
                created_at=datetime.utcnow(),
                c1_nota=c1["nota"], c1_obs=c1["obs"],
                c2_nota=c2["nota"], c2_obs=c2["obs"],
                c3_nota=c3["nota"], c3_obs=c3["obs"],
                c4_nota=c4["nota"], c4_obs=c4["obs"],
                c5_nota=c5["nota"], c5_obs=c5["obs"],
                stars=max(0, min(5, (c1["stars"]+c2["stars"]+c3["stars"]+c4["stars"]+c5["stars"]) // 5)),
                nota_total=nota_total,
                original_text=original_text  
            )

            self.db_session.add(essay)
            self.db_session.flush()   
            self.db_session.commit()
            return essay

        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(status_code=400, detail="Não foi possível salvar a redação (integridade).")
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"Falha ao salvar redação: {e}")

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
