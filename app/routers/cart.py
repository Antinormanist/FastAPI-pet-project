from typing import List

from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Cart, Banana
from app.routers.auth import get_current_user
from app import schemes

router = APIRouter(
    tags=['Cart'],
    prefix='/carts'
)


@router.get('/{id}', response_model=schemes.CartReturn)
def get_cart(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.id == id).first()
    if cart is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'cart with id {id} is not found')
    if cart.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'cart with id {id} is not your cart')
    return cart


@router.get('/', response_model=List[schemes.CartReturn])
def get_own_carts(db: Session = Depends(get_db), user = Depends(get_current_user)):
    carts = db.query(Cart).filter(Cart.owner_id == user.id)
    return carts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemes.CartReturn)
def create_cart(body: schemes.CartCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if db.query(Banana).filter(Banana.id == body.banana_id).first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'banana with id {body.banana_id} is not found')
    body = body.dict()
    body['owner_id'] = user.id
    cart = Cart(**body)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.id == id).first()
    if cart is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'cart with id {id} is not found')
    if cart.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'cart with id {id} is not your cart')
    db.delete(cart)
    db.commit()


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_all_carts(db: Session = Depends(get_db), user = Depends(get_current_user)):
    carts = db.query(Cart).filter(Cart.owner_id == user.id).delete()
    db.commit()