from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
load_dotenv()



# while True: # Done using SQLAlchemy
#     try:
#         conn = psycopg2.connect(host=os.getenv('HOST'), database=os.getenv('DATABASE'), user=os.getenv('USER'), password=os.getenv('PASSWORD'), cursor_factory=RealDictCursor)
#         curr = conn.cursor()
#         print("Database connection was successfull")
#         break

#     except Exception as er:
#         print("connecting to database failed")
#         print("Error:", str(er))
#         time.sleep(2)

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