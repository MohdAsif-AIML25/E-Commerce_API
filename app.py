import os
from app import create_app, db, migrate
from app.models.models import User, Product, Order, OrderItem

env = os.environ.get('FLASK_ENV', 'dev')
app = create_app(env)

@app.route('/')
def home():
    return {"message": "Welcome to the Ecommerce API. The server is healthy and running!"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
