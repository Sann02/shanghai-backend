# tests/test_categories.py
# The 'client' fixture is available from tests/conftest.py automatically


# ─── GET /categories ─────────────────────────────────────────────────
def test_get_all_categories(client):
    """GET /categories returns 200 and a list response."""
    response = client.get('/categories')

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_category_by_id(client):
    """GET /categories/1 returns 200 and correct data for seeded category."""
    response = client.get('/categories/1')

    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == 'Electronics'


def test_get_category_nonexistent_returns_404(client):
    """GET /categories/9999 returns 404 for non-existent ID."""
    response = client.get('/categories/9999')

    assert response.status_code == 404


# ─── POST /categories ────────────────────────────────────────────────
def test_create_category_returns_201(client):
    """POST /categories with valid name returns 201 and 'id' in response."""
    payload = {'name': 'Furniture'}
    response = client.post('/categories', json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['name'] == 'Furniture'


def test_create_category_missing_name_returns_400(client):
    """POST /categories without 'name' returns 400."""
    payload = {}
    response = client.post('/categories', json=payload)

    assert response.status_code == 400


# ─── PUT /categories/<id> ────────────────────────────────────────────
def test_update_category_returns_200(client):
    """PUT /categories/1 with new name returns 200 and updated name."""
    payload = {'name': 'Consumer Electronics'}
    response = client.put('/categories/1', json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Consumer Electronics'


def test_update_category_nonexistent_returns_404(client):
    """PUT /categories/9999 returns 404 for non-existent ID."""
    payload = {'name': 'Ghost Category'}
    response = client.put('/categories/9999', json=payload)

    assert response.status_code == 404


# ─── DELETE /categories/<id> ─────────────────────────────────────────
def test_delete_category_removes_it(client):
    """Create a throwaway category, delete it, confirm 404 on follow-up GET."""
    # 1. Create a throwaway category
    create_response = client.post('/categories', json={'name': 'Throwaway'})
    assert create_response.status_code == 201
    category_id = create_response.get_json()['id']

    # 2. Delete it
    delete_response = client.delete(f'/categories/{category_id}')
    assert delete_response.status_code == 200

    # 3. Confirm it's gone
    get_response = client.get(f'/categories/{category_id}')
    assert get_response.status_code == 404
