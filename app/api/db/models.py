from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy import JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.api.db.base import Base

class UserModel(Base):
  __tablename__ = "users"
  id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
  username = Column('username', String, nullable=False, unique = True)
  password = Column('password', String, nullable=False)
  analyses = relationship("UserEssaysModel", back_populates="user", cascade="all, delete-orphan")


class UserEssaysModel(Base):
  __tablename__ = "essay_analyses"
  id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
  user_id = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
  created_at = Column('created_at', DateTime, nullable=False, default=datetime.utcnow)
  input_text = Column('input_text', Text, nullable=False)
  c1_nota = Column('c1_nota', Integer, nullable=False)
  c1_obs = Column('c1_obs', Text, nullable=False)
  c2_nota = Column('c2_nota', Integer, nullable=False)
  c2_obs = Column('c2_obs', Text, nullable=False)
  c3_nota = Column('c3_nota', Integer, nullable=False)
  c3_obs = Column('c3_obs', Text, nullable=False)
  c4_nota = Column('c4_nota', Integer, nullable=False)
  c4_obs = Column('c4_obs', Text, nullable=False)
  c5_nota = Column('c5_nota', Integer, nullable=False)
  c5_obs = Column('c5_obs', Text, nullable=False)
  stars = Column('stars', Text, nullable=False)
  nota_total = Column('nota_total', Integer, nullable=False)
  user = relationship("UserModel", back_populates="analyses")
  

  
  
