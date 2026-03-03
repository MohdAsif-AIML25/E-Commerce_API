from flask import Blueprint, request, jsonify
from app.services.payment_service import PaymentService
from flask_jwt_extended import jwt_required
from app.models.models import Order

payment_blueprint = Blueprint('payment', __name__)

@payment_blueprint.route('/checkout/<int:order_id>', methods=['POST'])
@jwt_required()
def checkout(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    session_id, error = PaymentService.create_checkout_session(order.id, order.total_amount)
    if error:
        return jsonify({'message': error}), 500
    return jsonify(sessionId=session_id), 200
