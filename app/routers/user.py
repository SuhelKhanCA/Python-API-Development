from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import APIRouter


from ..schemas import UserCreate
from ..schemas import UserOut


from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

from ..utils import hash


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user : UserCreate , db : Session  = Depends(get_db)):

    # hash the password - user.password
    user.password = hash(user.password)

    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.get('/{id}', response_model=UserOut)
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} does not found")
    return user
