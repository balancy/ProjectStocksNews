from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import SQLALCHEMY_DATABASE_URI

# engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})
engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(bind=engine, autoflush=False))

Base = declarative_base()
Base.query = db_session.query_property()
