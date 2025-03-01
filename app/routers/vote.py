from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import APIRouter

from ..schemas import Vote


from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import oauth2


from ..utils import hash


router = APIRouter(
    prefix="/vote",
    tags = ['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id{vote.post_id} does not exits")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == curr_user.id)

    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {curr_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = curr_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}
