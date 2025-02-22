from fastapi import FastAPI
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

import time
import os
from dotenv import load_dotenv
load_dotenv()

from . import models
from .database import engine

from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


while True:
    try:
        conn = psycopg2.connect(host=os.getenv('HOST'), database=os.getenv('DATABASE'), user=os.getenv('USER'), password=os.getenv('PASSWORD'), cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print("Database connection was successfull")
        break

    except Exception as er:
        print("connecting to database failed")
        print("Error:", str(er))
        time.sleep(2)


@app.get("/")
async def root():

    return { "message" : "Welcome to my api"}
