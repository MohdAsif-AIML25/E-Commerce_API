from flask import Blueprint, request, jsonify
from app.services.services import AuthService, ProductService, OrderService
from app.schemas.schemas import UserSchema, ProductSchema, OrderSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import admin_required

# Auth Routes
auth_blueprint = Blueprint('auth', __name__)
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user, error = AuthService.register(data['name'], data['email'], data['password'])
    if error: return jsonify({'message': error}), 400
    return jsonify({'message': 'User registered successfully!'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result, error = AuthService.login(data['email'], data['password'])
    if error: return jsonify({'message': error}), 401
    return jsonify(token=result['token']), 200

# Product Routes
product_blueprint = Blueprint('product', __name__)
@product_blueprint.route('/', methods=['GET'])
def get_products():
    products = ProductService.get_all()
    return jsonify(ProductSchema(many=True).dump(products)), 200

@product_blueprint.route('/', methods=['POST'])
@admin_required
def create_product():
    data = request.get_json()
    product = ProductService.create(data['name'], data['description'], data['price'], data['stock'])
    return jsonify(ProductSchema().dump(product)), 201

# Order Routes
order_blueprint = Blueprint('order', __name__)
@order_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    order, error = OrderService.create_order(user_id, data['items'])
    if error: return jsonify({'message': error}), 400
    return jsonify(OrderSchema().dump(order)), 201

# Payment Routes
from app.services.payment_service import PaymentService
payment_blueprint = Blueprint('payment', __name__)
@payment_blueprint.route('/checkout/<int:order_id>', methods=['POST'])
@jwt_required()
def checkout(order_id):
    from app.models.models import Order
    order = Order.query.get(order_id)
    if not order: return jsonify({'message': 'Order not found'}), 404
    session_id, error = PaymentService.create_checkout_session(order.id, order.total_amount)
    if error: return jsonify({'message': error}), 500
    return jsonify(sessionId=session_id), 200
