def test_get_users(client, create_user):
    response = client.get('/users')
    assert response.status_code == 200
