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
def get_users(page: int = 1, db: Session = Depends(get_db)):
    if page < 1:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'page must be a positive integer')
    return db.query(User).offset((page - 1) * 20).limit(20)


@router.get('/{id}', response_model=schemes.UserReturn)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'user with id {id} is not found')
    return user


@router.post('/', response_model=schemes.UserReturn, status_code=status.HTTP_201_CREATED)
def create_user(body: schemes.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status.HTTP_409_CONFLICT, 'user with such username already exists')
    body.password = hash_password(body.password)
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put('/', response_model=schemes.UserReturn)
def full_update_user(body: schemes.UserUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status.HTTP_409_CONFLICT, 'user with such username already exists')
    for field, value in body.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.patch('/', response_model=schemes.UserReturn)
def partial_update_user(body: schemes.PartialUpdateUser, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status.HTTP_409_CONFLICT, 'user with such username already exists')
    for field, value in body.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'authorized user is not found')
    db.delete(user)
    db.commit()