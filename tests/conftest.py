import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

from app.database import Base, get_db
from app.routers.auth import create_access_token
from app.main import app

DBMS = config('DBMS')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST_TEST')
DB_NAME = config('DB_NAME')
SQLALCHEMY_URL = f'{DBMS}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}_test'

engine = create_engine(SQLALCHEMY_URL)
LocalSession = sessionmaker(bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def create_user(client):
    user_data = {'email': 'test@gmail.com', 'username': 'username', 'password': 'test'}
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(create_user):
    return create_access_token({'user_id': create_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers['Authorization'] = f'Bearer {token}'
    return client