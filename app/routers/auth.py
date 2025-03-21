from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas import UserLogin
from ..schemas import Token
from ..utils import verify
from .. import oauth2



router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=Token)
def login(user_creds : OAuth2PasswordRequestForm = Depends() ,db : Session = Depends(get_db)):

    #{
    # "username" : "asdfds"
    # "password" : "afas24124"
    # } 

    user = db.query(models.User).filter(models.User.email == user_creds.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invlaid Credentials")
    
    # create a token
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    
    # return token
    return {"access_token" : access_token, "token_type" : "bearer"}