from .database import Base
from sqlalchemy import Column, String, Integer

class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, nullable=False)
    email = Column('email', String, nullable=False)
    username = Column('username', String, unique=True, nullable=False)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    password = Column('password', String, nullable=False)
