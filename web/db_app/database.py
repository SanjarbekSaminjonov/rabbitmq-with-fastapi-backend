from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import env

SQLALCHEMY_DATABASE_URL = f"postgresql://{env.str('POSTGRES_USER')}:{env.str('POSTGRES_PASSWORD')}@postgres/{env.str('POSTGRES_DB')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
