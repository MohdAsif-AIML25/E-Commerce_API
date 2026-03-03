from flask import Blueprint, request, jsonify
from app.services.services import OrderService
from app.schemas.schemas import OrderSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

order_blueprint = Blueprint('order', __name__)

@order_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    order, error = OrderService.create_order(user_id, data.get('items'))
    if error:
        return jsonify({'message': error}), 400
    return jsonify(OrderSchema().dump(order)), 201
