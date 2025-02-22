from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker

import time
import os
from dotenv import load_dotenv
load_dotenv()


# URL ==> 'postgres://<username>:<password>@<IP-Address/hostname>/<db_name>'

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DATABASE')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close() 