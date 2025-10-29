# app/api/db/models.py
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, SmallInteger
from sqlalchemy.sql import func, text as sa_text
from sqlalchemy.orm import relationship
from app.api.db.base import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    analyses = relationship("UserEssaysModel", back_populates="user", cascade="all, delete-orphan")


class UserEssaysModel(Base):
    __tablename__ = "essay_analyses"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # server_default evita ter que mandar o created_at manualmente
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    input_text = Column(Text, nullable=False)

    c1_nota = Column(Integer, nullable=False)
    c1_obs  = Column(Text, nullable=False, server_default=sa_text("''"))
    c1_stars = Column(Integer, nullable=False)

    c2_nota = Column(Integer, nullable=False)
    c2_obs  = Column(Text, nullable=False, server_default=sa_text("''"))
    c2_stars = Column(Integer, nullable=False)

    c3_nota = Column(Integer, nullable=False)
    c3_obs  = Column(Text, nullable=False, server_default=sa_text("''"))
    c3_stars = Column(Integer, nullable=False)

    c4_nota = Column(Integer, nullable=False)
    c4_obs  = Column(Text, nullable=False, server_default=sa_text("''"))
    c4_stars = Column(Integer, nullable=False)

    c5_nota = Column(Integer, nullable=False)
    c5_obs  = Column(Text, nullable=False, server_default=sa_text("''"))
    c5_stars = Column(Integer, nullable=False)

    stars = Column(SmallInteger, nullable=False)

    nota_total = Column(Integer, nullable=False)

    user = relationship("UserModel", back_populates="analyses")
