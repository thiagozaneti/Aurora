import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_engine(url=DB_URL,pool_pre_ping=True)
Session = sessionmaker(bind = engine)
