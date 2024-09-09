from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, PositiveInt
from pydantic.types import confloat


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str


class UserUpdate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str


class PartialUpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None


class UserReturn(BaseModel):
    id: int
    email: EmailStr
    username: str
    wallet: float
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Banana(BaseModel):
    name: str
    description: Optional[str] = None
    price: confloat(ge=1)
    image: bytes


class BananaCreate(Banana):
    pass


class BananaReturn(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: confloat(ge=1)
    owner_id: PositiveInt
    owner: UserReturn
    created_at: datetime


class CartCreate(BaseModel):
    banana_id: PositiveInt


class CartReturn(BaseModel):
    id: int
    owner_id: PositiveInt
    owner: UserReturn
    banana_id: PositiveInt
    banana: BananaReturn
    created_at: datetime