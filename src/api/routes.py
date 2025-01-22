from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Customer
from src.services.kafka_producer import send_to_kafka

app = FastAPI()

from pydantic import BaseModel

class CustomerRequest(BaseModel):
    name: str
    email: str

@app.get("/checking")
def check_fun():
    return {"message": "this endpoint is working"}


@app.post("/customers/")
def create_customer(customer_request: CustomerRequest, db: Session = Depends(get_db)):
    customer = Customer(name=customer_request.name, email=customer_request.email)
    db.add(customer)
    db.commit()
    db.refresh(customer)

    send_to_kafka("customer_created", {"id": customer.id, "name": customer.name, "email": customer.email})
    return {"message": "Customer added and queued for sync"}
