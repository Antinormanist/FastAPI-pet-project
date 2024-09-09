from .database import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, text, ForeignKey, LargeBinary, Text, Numeric
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, nullable=False)
    email = Column('email', String, nullable=False)
    username = Column('username', String, unique=True, nullable=False)
    wallet = Column('wallet', Numeric(8, 2), default=0, nullable=False)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    password = Column('password', String, nullable=False)


class Banana(Base):
    __tablename__ = 'bananas'
    id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column('name', String, nullable=False)
    description = Column('description', Text)
    image = Column('image', LargeBinary, nullable=False)
    price = Column('price', Numeric(precision=8, scale=2), nullable=False)
    owner_id = Column('owner_id', ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User')
    created_at = Column('created_at', TIMESTAMP(timezone=True), default=text('now()'), nullable=False)


class Cart(Base):
    __tablename__ = 'carts'
    id = Column('id', Integer, primary_key=True, nullable=False)
    owner_id = Column('owner_id', ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User')
    banana_id = Column('banana_id', ForeignKey('bananas.id', ondelete='CASCADE'), nullable=False)
    banana = relationship('Banana')
    created_at = Column('created_at', TIMESTAMP(timezone=True), default=text('now()'), nullable=False)

