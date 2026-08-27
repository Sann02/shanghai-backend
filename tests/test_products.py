# tests/test_products.py
# conftest.py already provides the 'client' fixture


# ─── GET all products ────────────────────────────────────────────────
def test_get_all_products(client):
    response = client.get('/products')

    # Step 3: assert status code is 200
    assert response.status_code == 200

    # Step 4: parse JSON and assert it is a list with at least 1 item
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Step 5: assert the first item has keys 'id', 'name', 'price'
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'price' in data[0]


# ─── POST /products ──────────────────────────────────────────────────
def test_create_product_returns_201(client):
    payload = {'name': 'Keyboard', 'price': 49.99, 'category_id': 1}
    response = client.post('/products', json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['name'] == 'Keyboard'


def test_create_product_missing_name_returns_400(client):
    payload = {'price': 25.00, 'category_id': 1}
    response = client.post('/products', json=payload)

    assert response.status_code == 400


def test_create_product_negative_price_returns_400(client):
    payload = {'name': 'Bad Product', 'price': -10.0, 'category_id': 1}
    response = client.post('/products', json=payload)

    assert response.status_code == 400


# ─── GET /products/<id> ──────────────────────────────────────────────
def test_get_product_by_id_returns_200(client):
    response = client.get('/products/1')

    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == 'Laptop'


def test_get_product_nonexistent_returns_404(client):
    response = client.get('/products/9999')

    assert response.status_code == 404


# ─── PUT /products/<id> ──────────────────────────────────────────────
def test_update_product_returns_200(client):
    payload = {'price': 19.99}
    response = client.put('/products/2', json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data['price'] == 19.99
