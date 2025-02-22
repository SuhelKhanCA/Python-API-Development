from fastapi import Depends
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from fastapi import APIRouter

from typing import List

from ..schemas import PostCreate
from ..schemas import Post
from .. import oauth2



from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/",response_model=List[Post])
def get_posts(db : Session = Depends(get_db)):
    # curr.execute("""
    #                         SELECT * FROM posts
    #                     """)
    # posts = curr.fetchall()
    posts = db.query(models.Post).all()
    return  posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db : Session = Depends(get_db), user_id:int = Depends(oauth2.get_current_user)):
   
    # curr.execute('''INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING*''', (post.title, post.content, post.published))
    # new_post = curr.fetchone()
    # conn.commit()

    # print(post.dict())
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)


    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=Post)
def get_post(id : int, db : Session = Depends(get_db)):

    # curr.execute("""SELECT * FROM posts WHERE id= %s""", (id, ))
    # post = curr.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=Post)
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