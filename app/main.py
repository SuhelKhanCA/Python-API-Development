from fastapi import FastAPI
from fastapi import Response
from fastapi import status
from fastapi import HTTPException


from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor

import time
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

class Post(BaseModel):

    title:str
    content:str
    published : bool = True

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
 

my_posts = [{"title" : "Title of post 1", "content" : "Content of post 1", "id": 1}, {"title" : "Title of post 2", "content" : "Content of post 2", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, p in enumerate(my_posts):            
        if p['id'] == id:
            return i


@app.get("/")
async def root():

    return { "message" : "Welcome to my api"}


@app.get("/posts")
def get_posts():
    curr.execute("""
                            SELECT * FROM posts
                        """)
    posts = curr.fetchall()
    print(posts)
    return {"data" : posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
   
    curr.execute('''INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING*''', (post.title, post.content, post.published))
    new_post = curr.fetchone()
    conn.commit()

    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id : int):

    curr.execute("""SELECT * FROM posts WHERE id= %s""", (id, ))
    post = curr.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    return { "post_detail" : post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    curr.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    post_deleted = curr.fetchone()
    conn.commit()

    print(post_deleted)

    if post_deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: Post):
    
    curr.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id =%s RETURNING *""", (post.title, post.content, post.published, id))
    
    updated_post = curr.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exits")

    return {"data" : updated_post}

    