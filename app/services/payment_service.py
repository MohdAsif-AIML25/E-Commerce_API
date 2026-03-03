import stripe
from flask import current_app

class PaymentService:
    @staticmethod
    def create_checkout_session(order_id, amount):
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(amount * 100),
                        'product_data': {'name': f'Order #{order_id}'},
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:3000/success',
                cancel_url='http://localhost:3000/cancel',
            )
            return checkout_session.id, None
        except Exception as e:
            return None, str(e)
