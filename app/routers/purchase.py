from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Cart, User
from app.routers.auth import get_current_user
from app import schemes

router = APIRouter(
    tags=['Purchase'],
    prefix='/purchase'
)


@router.post('/')
def buy_products(buy: bool, db: Session = Depends(get_db), user = Depends(get_current_user)):
    products = db.query(Cart).filter(Cart.owner_id == user.id)
    total_price = 0
    bananas = []
    for prod in products:
        total_price += prod.banana.price
        bananas.append(prod.banana.name)
    if total_price < user.wallet:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, f'you don\'t have enough money. You have {user.wallet} you need to have {total_price}')
    user.wallet -= total_price
    for prod in products:
        id = prod.owner_id
        us = db.query(User).filter(User.id == id).first()
        if us:
            us.wallet += prod.price
    products.delete()
    db.commit()
    return {'message': 'You successfully bought it.'}