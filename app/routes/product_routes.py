from flask import Blueprint, request, jsonify
from app.services.services import ProductService
from app.schemas.schemas import ProductSchema
from app.utils.decorators import admin_required

product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/', methods=['GET'])
def get_products():
    products = ProductService.get_all()
    return jsonify(ProductSchema(many=True).dump(products)), 200

@product_blueprint.route('/', methods=['POST'])
@admin_required
def create_product():
    data = request.get_json()
    product = ProductService.create(data.get('name'), data.get('description'), data.get('price'), data.get('stock'))
    return jsonify(ProductSchema().dump(product)), 201
