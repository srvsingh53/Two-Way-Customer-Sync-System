import stripe
from src.config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

def create_customer(name, email):
    try:
        customer = stripe.Customer.create(
            name=name,
            email=email
        )
        print(f"Customer created: {customer}") 
        return customer['id']
    except Exception as e:
        print(f"Error creating customer: {e}")
        return None
