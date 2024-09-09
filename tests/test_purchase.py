def test_invalid_buy_products(authorized_client, create_cart):
    response = authorized_client.post('/purchase')
    assert response.status_code == 422


# def test_buy_products(create_cart, authorized_client, create_user):
#     authorized_client.get('/purchase/money')
#     response = authorized_client.post('/purchase')
#     assert response.status_code == 200
#     assert response.json()['message'] == 'You successfully bought it.'