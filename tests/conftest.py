import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

from app.database import Base, get_db
from app.routers.auth import create_access_token
from app.main import app
from app import schemes

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
def create_user2(client):
    user_data = {'email': 'qtest@gmail.com', 'username': 'qusername', 'password': 'test'}
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
def token2(create_user2):
    return create_access_token({'user_id': create_user2['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers['Authorization'] = f'Bearer {token}'
    return client


@pytest.fixture
def authorized_client2(client, token2):
    client.headers['Authorization'] = f'Bearer {token2}'
    return client


@pytest.fixture
def create_banana(authorized_client):
    path = 'static/test_cucumber.png'
    with open(path, 'rb') as img:
        files = {'image': ('cucumber.png', img, 'image/png')}
        banana_data = {
            'name': 'freenana',
            'description': 'only com com com',
            'price': 998.99,
        }
        response = authorized_client.post('/bananas', data=banana_data, files=files)
        img.seek(0)
        original = img.read()
        response2 = authorized_client.get('/bananas/1/image')
        assert original == response2.content

    assert response.status_code == 201
    assert response.json()['name'] == banana_data['name']
    return response.json()


@pytest.fixture
def create_banana2(authorized_client2):
    path = 'static/test_cucumber.png'
    with open(path, 'rb') as img:
        files = {'image': ('cucumber.png', img, 'image/png')}
        banana_data = {
            'name': 'Antinana',
            'description': 'No com',
            'price': 111.11,
        }
        response = authorized_client2.post('/bananas', data=banana_data, files=files)
        img.seek(0)
        original = img.read()
        response2 = authorized_client2.get('/bananas/1/image')
        assert original == response2.content

    assert response.status_code == 201
    assert response.json()['name'] == banana_data['name']
    return response.json()


@pytest.fixture
def create_cart(authorized_client, create_user, create_banana):
    response = authorized_client.post('/carts', json={'banana_id': create_banana['id']})
    assert response.json()['banana_id'] == create_banana['id']
    assert response.json()['owner_id'] == create_user['id']
    return response.json()


@pytest.fixture
def create_cart2(authorized_client2, create_user2, create_banana2):
    response = authorized_client2.post('/carts', json={'banana_id': create_banana2['id']})
    assert response.json()['banana_id'] == create_banana2['id']
    assert response.json()['owner_id'] == create_user2['id']
    return response.json()
