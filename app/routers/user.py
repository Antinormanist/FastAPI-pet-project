from typing import List

from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user
from app.utils import hash_password
from app import schemes

router = APIRouter(
    tags=['User'],
    prefix='/users'
)


@router.get('/', response_model=List[schemes.UserReturn])
def get_users(page=1, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(User).offset((page - 1) * 50).limit(50)


@router.post('/', response_model=schemes.UserReturn)
def create_user(body: schemes.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status.HTTP_409_CONFLICT, 'user with such username already exists')
    body.password = hash_password(body.password)
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user