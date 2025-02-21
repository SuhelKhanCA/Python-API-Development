from fastapi import FastAPI
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


class Post(BaseModel):

    title:str
    content:str
    published : bool = True
    rating : Optional[int] = None


app = FastAPI()

my_posts = [{"title" : "Title of post 1", "content" : "Content of post 1", "id": 1}, {"title" : "Title of post 2", "content" : "Content of post 2", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/")
async def root():

    return { "message" : "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data" : my_posts}


@app.post("/posts")
def create_posts(post: Post):

    post_dict = post.model_dump()
    post_dict['id'] = randrange(3, 100000)
    
    my_posts.append(post_dict)
    return {"data" : post_dict}

@app.get("/posts/{id}")
def get_post(id : int, response : Response):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id: {id} was not found"}
    return { "post_detail" : post}