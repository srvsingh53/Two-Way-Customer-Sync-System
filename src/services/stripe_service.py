
import stripe
from src.config.settings import STRIPE_SECRET_KEY

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stripe.api_key = STRIPE_SECRET_KEY

def find_existing_customer(email):
    
    customers = stripe.Customer.list(email=email).data
    return customers[0] if customers else None

def create_customer(name, email):
    existing_customer = find_existing_customer(email)
    if existing_customer:
        logger.info(f"Customer already exists: {existing_customer['id']}")
        return existing_customer['id']
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
