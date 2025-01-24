from fastapi import APIRouter, Request, HTTPException, Header
import stripe
import os
from src.database.db import SessionLocal
from src.database.models import Customer
import logging

router = APIRouter()

# Load Stripe keys from environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, webhook_secret
        )
    except ValueError:
        logging.error("Invalid payload received.")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        logging.error("Invalid signature verification.")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle Stripe events
    if event["type"] == "customer.created" or event["type"] == "customer.updated":
        customer_data = event["data"]["object"]
        db = SessionLocal()
        customer = db.query(Customer).filter_by(email=customer_data["email"]).first()

        if not customer:
            new_customer = Customer(name=customer_data["name"], email=customer_data["email"])
            db.add(new_customer)
        else:
            customer.name = customer_data["name"]

        db.commit()
        db.close()
        logging.info(f"Customer {customer_data['email']} synced from Stripe.")

    return {"status": "success"}
