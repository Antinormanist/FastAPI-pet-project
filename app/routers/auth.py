import datetime
from datetime import timedelta, timezone, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from decouple import config

from app.database import get_db
from app.models import User
from app.utils import verify_password

router = APIRouter()

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
EXPIRE_TIME_MINUTES = config('EXPIRE_TIME_MINUTES', cast=int)

oauth2 = OAuth2PasswordBearer(tokenUrl='/login')

def create_access_token(body: dict):
    to_encode = body.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_TIME_MINUTES) if EXPIRE_TIME_MINUTES else timedelta(minutes=60)
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload['user_id']
        if id is None:
            raise credentials_exception
    except:
        raise credentials_exception
    return id


def get_current_user(token: str = Depends(oauth2), bd: Session = Depends(get_db)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, 'Could not validate credentials')
    id = verify_token(token, credentials_exception)
    user = bd.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Can\'t find authorized user')
    return user


@router.post('/login')
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if user is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Invalid credentials')
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Invalid credentials')
    access_token = create_access_token({'user_id': user.id})
    return {'token': access_token, 'token_type': 'bearer'}