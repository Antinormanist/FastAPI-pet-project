USER_DATA = {
    'email': 'test@gmail.com',
    'username': 'username',
    'first_name': 'test',
    'last_name': 'test',
    'password': 'test'
}


def test_get_users(client, create_user):
    response = client.get('/users')
    assert response.status_code == 200


def test_get_users_next_page(client):
    for i in range(21):
        user_data = USER_DATA.copy()
        user_data['username'] = str(i)
        client.post('/users', json=user_data)
    response = client.get('/users?page=2')
    response = response.json()
    assert len(response) == 1
    assert response[0]['id'] == 21


def test_get_users_invalid_page(client):
    response = client.get('/users/?page=0')
    assert response.status_code == 400


def test_get_user_by_id(client, create_user):
    response = client.get(f'/users/{create_user['id']}')
    assert response.status_code == 200
    assert response.json()['username'] == create_user['username']
    assert response.json()['wallet'] == create_user['wallet']


def test_get_invalid_user_by_id(client):
    response = client.get('/users/1')
    assert response.status_code == 404


def test_create_existed_user(client, create_user):
    user_data = USER_DATA.copy()
    user_data['username'] = create_user['username']
    response = client.post('/users/', json=user_data)
    assert response.status_code == 409


def test_update_user(authorized_client):
    user_data = USER_DATA.copy()
    user_data['username'] = 'test_username'
    response = authorized_client.put('/users/', json=user_data)
    assert response.status_code == 200
    assert response.json()['username'] == user_data['username']


def test_update_on_existed_user(authorized_client, create_user):
    user_data = USER_DATA.copy()
    response = authorized_client.put('/users/', json=user_data)
    assert response.status_code == 409


def test_partial_update_user(authorized_client, create_user):
    user_data = {
        'email': 'differentemail@gmail.com'
    }
    response = authorized_client.patch('/users/', json=user_data)
    assert response.status_code == 200
    assert response.json()['email'] == user_data['email']


def test_partial_update_on_existed_user(authorized_client, create_user):
    user_data = {
        'username': create_user['username']
    }
    response = authorized_client.patch('/users/', json=user_data)
    assert response.status_code == 409


def test_delete_user(authorized_client):
    response = authorized_client.delete('/users/')
    assert response.status_code == 204