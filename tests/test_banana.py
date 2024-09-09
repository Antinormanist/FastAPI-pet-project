from venv import create


def test_get_bananas(client):
    response = client.get('/bananas/')
    assert response.status_code == 200


def test_get_banana(client, create_banana):
    response = client.get('/bananas/1')
    assert response.status_code == 200
    assert response.json()['name'] == create_banana['name']


def test_update_banana(authorized_client, create_banana):
    with open('static/banana.png', 'rb') as img:
        banana_data = {
            'name': 'anana',
            'description': 'qwe',
            'price': 200,
        }
        files = {'image': ('banana.png', img, 'image/png')}
        response = authorized_client.put(f'/bananas/{create_banana['id']}', data=banana_data, files=files)
        image = authorized_client.get(f'/bananas/{create_banana['id']}/image')
        img.seek(0)
        assert response.status_code == 200
        assert image.content == img.read()
        assert response.json()['name'] == banana_data['name']


def test_forbidden_update_banana(create_banana, authorized_client2):
    with open('static/banana.png', 'rb') as img:
        banana_data = {
            'name': 'anana',
            'description': 'qwe',
            'price': 200,
        }
        files = {'image': ('banana.png', img, 'image/png')}
        response = authorized_client2.put(f'/bananas/{create_banana['id']}', data=banana_data, files=files)
        assert response.status_code == 403


def test_partial_update_banana(authorized_client, create_banana):
    with open('static/banana.png', 'rb') as img:
        banana_data = {
            'name': 'anana'
        }
        files = {'image': ('banana.png', img, 'image/png')}
        response = authorized_client.patch(f'/bananas/{create_banana['id']}', data=banana_data, files=files)
        image = authorized_client.get(f'/bananas/{create_banana['id']}/image')
        img.seek(0)
        assert response.status_code == 200
        assert image.content == img.read()
        assert response.json()['name'] == banana_data['name']
        assert response.json()['description'] == create_banana['description']


def test_forbidden_partial_update_banana(create_banana, authorized_client2):
    with open('static/banana.png', 'rb') as img:
        banana_data = {
            'name': 'anana'
        }
        files = {'image': ('banana.png', img, 'image/png')}
        response = authorized_client2.patch(f'/bananas/{create_banana['id']}', data=banana_data, files=files)
        assert response.status_code == 403


def test_delete_banana(authorized_client, create_banana):
    response = authorized_client.delete(f'/bananas/{create_banana['id']}/')
    assert response.status_code == 204
    response = authorized_client.get(f'/bananas/{create_banana['id']}/')
    assert response.status_code == 404


def test_forbidden_delete_banana(create_banana, authorized_client2):
    response = authorized_client2.delete(f'/bananas/{create_banana['id']}/')
    assert response.status_code == 403
