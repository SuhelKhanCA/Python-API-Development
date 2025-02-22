from fastapi import Depends
from fastapi import status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

import os
from dotenv import load_dotenv

load_dotenv()

# SECRET KEY
# Algorithm
# Expiration time
key = os.getenv('SECRET_KEY')
algo = os.getenv('ALGORITHM')
exp_time = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


def create_access_token(data:dict):

    data_to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=exp_time)
    data_to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(data_to_encode, key, algorithm=algo)

    return encoded_jwt

def verify_access_token(token:str, credentials_exception):

    try:
        payload = jwt.decode(token=token, key=key, algorithms=[algo])

        id:str = payload.get('user_id')

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data

# get the specific user
def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)