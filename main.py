from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):

    title:str
    content:str
    published : bool = True
    rating : Optional[int] = None


app = FastAPI()


# request GET method url: "/"

@app.get("/")
async def root():

    # return { "message" : "Hello world"}
    return { "message" : "Welcome to my my api"}

# Order matters
# @app.get("/")
# def posts():
#     return {"data" : "These are your posts!"}

@app.get("/posts")
def posts():
    return {"data" : "These are your posts!"}



# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):

#     print(payload) # printing in the console
#     return {
#         "new_post" : {
#             "data" : {
#                 "title" : f"{payload['title']}",
#                 "content" : f"{payload['content']}"
#             }
#         }
#     }


# title str, content str
@app.post("/createposts")
def create_posts(post: Post):
    
    print(post)
    print(post.dict()) # depricated
    print(post.model_dump()) # new way

    print(post.published)
    print(post.rating)
    print(type(post)) # Post

    return {"data" : post}