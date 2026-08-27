# app/routes.py
from flask import Blueprint, jsonify, request
from app import db
from app.models import Product, Category

products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def get_all_products():
    """Return all products as JSON list."""
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200


@products_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product. Expects JSON with name, price, category_id."""
    data = request.get_json()

    # Validate required fields
    if not data or 'name' not in data or not data['name']:
        return jsonify({'error': 'name is required'}), 400

    if 'price' not in data:
        return jsonify({'error': 'price is required'}), 400

    if data['price'] < 0:
        return jsonify({'error': 'price must be non-negative'}), 400

    product = Product(
        name=data['name'],
        price=data['price'],
        category_id=data.get('category_id', 1),
    )
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """Return a single product by ID."""
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({'error': 'product not found'}), 404
    return jsonify(product.to_dict()), 200


@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product."""
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({'error': 'product not found'}), 404

    data = request.get_json()

    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'category_id' in data:
        product.category_id = data['category_id']

    db.session.commit()

    return jsonify(product.to_dict()), 200


# ─── Category Endpoints ──────────────────────────────────────────────

@products_bp.route('/categories', methods=['GET'])
def get_all_categories():
    """Return all categories as JSON list."""
    categories = Category.query.all()
    return jsonify([cat.to_dict() for cat in categories]), 200


@products_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    """Return a single category by ID."""
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({'error': 'category not found'}), 404
    return jsonify(category.to_dict()), 200


@products_bp.route('/categories', methods=['POST'])
def create_category():
    """Create a new category. Expects JSON with name."""
    data = request.get_json()

    if not data or 'name' not in data or not data['name']:
        return jsonify({'error': 'name is required'}), 400

    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_dict()), 201


@products_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update an existing category."""
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({'error': 'category not found'}), 404

    data = request.get_json()

    if 'name' in data:
        category.name = data['name']

    db.session.commit()

    return jsonify(category.to_dict()), 200


@products_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category by ID."""
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({'error': 'category not found'}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': 'category deleted'}), 200
