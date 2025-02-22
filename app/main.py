from fastapi import Depends, FastAPI
from fastapi import Response
from fastapi import status
from fastapi import HTTPException

from typing import Optional, List

from fastapi.params import Body
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

import time
import os
from dotenv import load_dotenv
load_dotenv()

from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .database import get_db

from .schemas import PostBase, UserOut
from .schemas import PostCreate
from .schemas import Post
from .schemas import UserCreate

from .utils import hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



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


@app.get("/posts",response_model=List[Post])
def get_posts(db : Session = Depends(get_db)):
    # curr.execute("""
    #                         SELECT * FROM posts
    #                     """)
    # posts = curr.fetchall()
    posts = db.query(models.Post).all()
    return  posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db : Session = Depends(get_db)):
   
    # curr.execute('''INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING*''', (post.title, post.content, post.published))
    # new_post = curr.fetchone()
    # conn.commit()

    # print(post.dict())
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print(new_post)
    return new_post

@app.get("/posts/{id}", response_model=Post)
def get_post(id : int, db : Session = Depends(get_db)):

    # curr.execute("""SELECT * FROM posts WHERE id= %s""", (id, ))
    # post = curr.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db)):
    # curr.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post_deleted = curr.fetchone()
    # conn.commit()

    post_qeury = db.query(models.Post).filter(models.Post.id == id)


    if post_qeury.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    post_qeury.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=Post)
def update_post(id: int, updated_post: PostCreate, db : Session = Depends(get_db)):
    
    # curr.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id =%s RETURNING *""", (post.title, post.content, post.published, id))
    # updated_post = curr.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exits")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# User registration

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user : UserCreate , db : Session  = Depends(get_db)):

    # hash the password - user.password
    user.password = hash(user.password)

    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@app.get('/users/{id}', response_model=UserOut)
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} does not found")
    return user