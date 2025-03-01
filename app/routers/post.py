from fastapi import Depends
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from fastapi import APIRouter

from typing import List, Optional

from sqlalchemy import func

from ..schemas import PostCreate, PostOut
from ..schemas import Post
from .. import oauth2
from .. import models



from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# @router.get("/",response_model=List[Post])
@router.get("/",response_model=List[PostOut])
def get_posts(db : Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0, search:Optional[str] = ""):
    # curr.execute("""
    #                         SELECT * FROM posts
    #                     """)
    # posts = curr.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()

    # SQL Join output
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()

    return  results

@router.get("/{id}", response_model=PostOut)
def get_post(id : int, db : Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):

    # curr.execute("""SELECT * FROM posts WHERE id= %s""", (id, ))
    # post = curr.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db : Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
   
    # curr.execute('''INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING*''', (post.title, post.content, post.published))
    # new_post = curr.fetchone()
    # conn.commit()

    # print(post.dict())
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)

    print(curr_user.id)
    new_post = models.Post(owner_id=curr_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    # curr.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post_deleted = curr.fetchone()
    # conn.commit()

    print(curr_user.id)
    post_qeury = db.query(models.Post).filter(models.Post.id == id)
    post = post_qeury.first()    
    print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_qeury.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=Post)
def update_post(id: int, updated_post: PostCreate, db : Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    # curr.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id =%s RETURNING *""", (post.title, post.content, post.published, id))
    # updated_post = curr.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exits")
    
    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()