# tests/conftest.py
import pytest
from flask_jwt_extended import create_access_token

from app import create_app, init_app, db as _db
from app.models import Product, Category, User, Order, OrderProduct
from app.middleware.auth import hash_password


# ══════════════════════════════════════════════════════════════════════════════
# Full-app (session-scoped) — used by new tests (test_product, test_user,
# test_order, test_create_order) via seed_* fixtures
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope='session')
def full_app():
    """Create the full application with JWT, controllers, etc."""
    flask_app = init_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-secret-key',
    })

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.session.remove()
        _db.drop_all()


# ══════════════════════════════════════════════════════════════════════════════
# Legacy app (module-scoped) — used by test_products, test_categories
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope='module')
def app():
    """Create simple application for legacy tests."""
    flask_app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with flask_app.app_context():
        _db.create_all()

        # Seed one Category and two Products
        cat = Category(name='Electronics')
        _db.session.add(cat)
        _db.session.commit()

        product1 = Product(name='Laptop', price=999.99, category_id=cat.id)
        product2 = Product(name='Mouse', price=29.99, category_id=cat.id)
        _db.session.add_all([product1, product2])
        _db.session.commit()

        yield flask_app

        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    """Test client — used by legacy tests (test_products, test_categories)."""
    return app.test_client()


# ══════════════════════════════════════════════════════════════════════════════
# Seed fixtures (function-scoped with cleanup) — new tests
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture()
def seed_users(full_app):
    """Seed test users: seller_jane (id=1), buyer_john (id=2), admin_bob (id=3)."""
    with full_app.app_context():
        users = [
            User(
                username='seller_jane',
                email='jane@example.com',
                password_hash=hash_password('password123'),
                role='seller',
            ),
            User(
                username='buyer_john',
                email='john@example.com',
                password_hash=hash_password('password123'),
                role='user',
            ),
            User(
                username='admin_bob',
                email='bob@example.com',
                password_hash=hash_password('password123'),
                role='admin',
            ),
        ]
        _db.session.add_all(users)
        _db.session.commit()

        yield users

        # Cleanup
        _db.session.rollback()
        User.query.delete()
        _db.session.commit()


@pytest.fixture()
def seed_products(full_app):
    """Seed test products and categories."""
    with full_app.app_context():
        cat1 = Category(name='Electronics')
        cat2 = Category(name='Clothing')
        _db.session.add_all([cat1, cat2])
        _db.session.commit()

        products = [
            Product(
                name='Wireless Mouse',
                sku='ELEC-001',
                description='A comfortable wireless mouse',
                price=29.99,
                stock_qty=50,
                is_active=True,
                category_id=cat1.id,
            ),
            Product(
                name='Mechanical Keyboard',
                sku='ELEC-002',
                description='RGB mechanical keyboard',
                price=89.99,
                stock_qty=30,
                is_active=True,
                category_id=cat1.id,
            ),
            Product(
                name='Cotton T-Shirt',
                sku='CLTH-001',
                description='100% cotton t-shirt',
                price=15.00,
                stock_qty=100,
                is_active=True,
                category_id=cat2.id,
            ),
            Product(
                name='Broken Headphones',
                sku='ELEC-003',
                description='These headphones are broken',
                price=49.99,
                stock_qty=5,
                is_active=False,
                category_id=cat1.id,
            ),
        ]
        _db.session.add_all(products)
        _db.session.commit()

        yield products

        # Cleanup
        _db.session.rollback()
        Product.query.delete()
        Category.query.delete()
        _db.session.commit()


@pytest.fixture()
def seed_orders(full_app, seed_users, seed_products):
    """Seed test orders for buyer_john (user_id=2)."""
    with full_app.app_context():
        users = seed_users
        products = seed_products
        buyer = users[1]  # buyer_john

        # Order 1: Wireless Mouse + Mechanical Keyboard = 119.98
        order1 = Order(user_id=buyer.id, total=119.98, status='pending')
        _db.session.add(order1)
        _db.session.flush()

        item1 = OrderProduct(order_id=order1.id, product_id=products[0].id, quantity=1)
        item2 = OrderProduct(order_id=order1.id, product_id=products[1].id, quantity=1)
        _db.session.add_all([item1, item2])

        # Order 2: Cotton T-Shirt = 15.00
        order2 = Order(user_id=buyer.id, total=15.00, status='completed')
        _db.session.add(order2)
        _db.session.flush()

        item3 = OrderProduct(order_id=order2.id, product_id=products[2].id, quantity=1)
        _db.session.add(item3)

        _db.session.commit()

        yield [order1, order2]

        # Cleanup
        _db.session.rollback()
        OrderProduct.query.delete()
        Order.query.delete()
        _db.session.commit()


# ─── Token fixtures ───────────────────────────────────────────────────────────

@pytest.fixture()
def seller_token(full_app, seed_users):
    """JWT access token for seller_jane (id=1, role=seller)."""
    with full_app.app_context():
        return create_access_token(
            identity='1',
            additional_claims={'role': 'seller'},
        )


@pytest.fixture()
def user_token(full_app, seed_users):
    """JWT access token for buyer_john (id=2, role=user)."""
    with full_app.app_context():
        return create_access_token(
            identity='2',
            additional_claims={'role': 'user'},
        )


@pytest.fixture()
def admin_token(full_app, seed_users):
    """JWT access token for admin_bob (id=3, role=admin)."""
    with full_app.app_context():
        return create_access_token(
            identity='3',
            additional_claims={'role': 'admin'},
        )
