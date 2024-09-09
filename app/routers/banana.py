from typing import List
from io import BytesIO

from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from fastapi.responses import  StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Banana
from app.routers.auth import get_current_user
from app import schemes

router = APIRouter(
    tags=['Banana'],
    prefix='/bananas'
)


@router.get('/', response_model=List[schemes.BananaReturn])
def get_bananas(page: int = 1, db: Session = Depends(get_db)):
    limit = 20
    return db.query(Banana).offset((page - 1) * limit).limit(limit)


@router.get('/{id}', response_model=schemes.BananaReturn)
def get_banana(id: int, db: Session = Depends(get_db)):
    banana = db.query(Banana).filter(Banana.id == id).first()
    if banana is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'banana with id {id} is not found')
    return banana


@router.get('/{id}/image')
async def get_banana_image(id: int, db: Session = Depends(get_db)):
    banana = db.query(Banana).filter(Banana.id == id).first()
    if banana is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'banana with id {id} is not found')
    if banana.image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'image is not found')
    return StreamingResponse(BytesIO(banana.image), media_type='image/jpeg')


@router.post('/', response_model=schemes.BananaReturn, status_code=status.HTTP_201_CREATED)
async def create_banana(
        name: str = Form(...),
        description: str = Form(None),
        price: float = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db),
        user = Depends(get_current_user)
    ):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image type")
    image_data = await image.read()
    banana = Banana(
        name=name,
        description=description,
        price=price,
        image=image_data,
        owner_id=user.id
    )
    db.add(banana)
    db.commit()
    db.refresh(banana)
    return banana


@router.put('/{id}', response_model=schemes.BananaReturn)
async def full_update_banana(
        id: int,
        name: str = Form(...),
        description: str = Form(...),
        price: int = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db),
        user = Depends(get_current_user)
    ):
    image_data = await image.read()
    banana = db.query(Banana).filter(Banana.id == id).first()
    if banana is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'banana with id {id} is not found')
    if banana.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'banana with id {id} is not your banana')
    banana.name = name
    banana.description = description
    banana.price = price
    banana.image = image_data
    db.commit()
    db.refresh(banana)
    return banana


@router.patch('/{id}', response_model=schemes.BananaReturn)
async def partial_update_banana(
        id: int,
        name: str = Form(None),
        description: str = Form(None),
        price: int = Form(None),
        image: UploadFile = File(None),
        db: Session = Depends(get_db),
        user = Depends(get_current_user)
    ):
    banana = db.query(Banana).filter(Banana.id == id).first()
    if banana is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'banana with id {id} is not found')
    if banana.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'banana with id {id} is not your banana')
    if name:
        banana.name = name
    if description:
        banana.description = description
    if price:
        banana.price = price
    if image:
        banana.image = await image.read()
    db.commit()
    db.refresh(banana)
    return banana


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_banana(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    banana = db.query(Banana).filter(Banana.id == id).first()
    if banana is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'banana with id {id} is not found')
    if banana.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'banana with id {id} is not your banana')
    db.delete(banana)
    db.commit()
