# app/models.py
from datetime import datetime, timezone
from app import db


# ─── Category ─────────────────────────────────────────────────────────────────

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return f'<Category {self.name}>'


# ─── Product ──────────────────────────────────────────────────────────────────

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock_qty = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    order_items = db.relationship('OrderProduct', backref='product', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category_id': self.category_id,
        }

    def __repr__(self):
        return f'<Product {self.name}>'


# ─── User ─────────────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    orders = db.relationship('Order', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
        }

    def __repr__(self):
        return f'<User {self.username}>'


# ─── Order ────────────────────────────────────────────────────────────────────

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    order_items = db.relationship('OrderProduct', backref='order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total': self.total,
            'status': self.status,
        }

    def __repr__(self):
        return f'<Order {self.id}>'


# ─── OrderProduct (many-to-many with quantity) ────────────────────────────────

class OrderProduct(db.Model):
    __tablename__ = 'order_products'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<OrderProduct order={self.order_id} product={self.product_id}>'
