def test_get_carts(authorized_client, create_banana, create_user, create_cart):
    response = authorized_client.get('/carts')
    response = response.json()[0]
    assert response['banana']['id'] == create_banana['id']
    assert response['owner']['id'] == create_user['id']


def test_get_cart(authorized_client, create_cart):
    response = authorized_client.get(f'/carts/{create_cart['id']}/')
    assert response.status_code == 200
    assert response.json()['id'] == create_cart['id']


def test_get_forbidden_cart(create_cart, authorized_client2):
    response = authorized_client2.get(f'/carts/{create_cart['id']}/')
    assert response.status_code == 403


def test_delete_cart(authorized_client, create_cart):
    response = authorized_client.delete(f'/carts/{create_cart['id']}/')
    assert response.status_code == 204
    response = authorized_client.get(f'/carts/{create_cart['id']}/')
    assert response.status_code == 404


def test_delete_forbidden_cart(create_cart, authorized_client2):
    response = authorized_client2.delete(f'/carts/{create_cart['id']}/')
    assert response.status_code == 403


def test_delete_all_carts(authorized_client, create_cart, create_banana):
    cart2 = authorized_client.post('/carts', json={'banana_id': create_banana['id']}).json()
    response = authorized_client.delete('/carts/')
    assert response.status_code == 204
    response = authorized_client.get(f'/carts/{create_cart['id']}/')
    assert response.status_code == 404
    response = authorized_client.get(f'/carts/{cart2['id']}/')
    assert response.status_code == 404