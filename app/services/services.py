from app.models.models import User, Product, Order, OrderItem
from app import db
from app.utils.security import Security
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def register(name, email, password):
        user = User.query.filter_by(email=email).first()
        if user:
            return None, "Email already exists"
        new_user = User(name=name, email=email, password=Security.hash_password(password))
        db.session.add(new_user)
        db.session.commit()
        return new_user, None

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if user and Security.check_password_hash(user.password, password):
            token = create_access_token(identity=user.id)
            return {'user': user, 'token': token}, None
        return None, "Invalid credentials"

class ProductService:
    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def create(name, description, price, stock):
        product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        return product

class OrderService:
    @staticmethod
    def create_order(user_id, items_data):
        total_amount = 0
        order_items = []
        for item in items_data:
            product = Product.query.get(item['product_id'])
            if not product or product.stock < item['quantity']:
                return None, f"Insufficient stock for {product.name if product else 'product'}"
            
            total_amount += product.price * item['quantity']
            order_items.append(OrderItem(product_id=product.id, quantity=item['quantity'], price=product.price))
            product.stock -= item['quantity']
        
        order = Order(user_id=user_id, total_amount=total_amount)
        order.items = order_items
        db.session.add(order)
        db.session.commit()
        return order, None
