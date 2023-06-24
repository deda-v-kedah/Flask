from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, func
from dotenv import load_dotenv
import os

load_dotenv()

pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')
pg_db = os.getenv('PG_DB')


engine = create_engine(f"postgresql://{pg_user}:{pg_password}@127.0.0.1:5432/{pg_db}")
Session = sessionmaker(bind=engine)
class Base(DeclarativeBase): pass


class Ads(Base):
    __tablename__ = "ads"

    ad_id = Column(Integer, primary_key=True, autoincrement=True)
    ad_title = Column(String, nullable=False, index=True)
    ad_description = Column(String)
    ad_creation_time = Column(DateTime, server_default=func.now())
    ad_creator = Column(Integer)


class Users(Base):
    __tablename__ = "our_users"

    user_id = Column(Integer,  primary_key=True, autoincrement=True)
    user_mail = Column(String,  nullable=False,  unique=True)
    user_password = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)