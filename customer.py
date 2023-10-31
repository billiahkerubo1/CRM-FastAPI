# customer.py
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer
from retrying import retry
from app.schema import CustomerCreate
#from fastapi.middleware.throttle import ThrottleLimiter

app = FastAPI()
customer_router = APIRouter()

# Define a custom retry strategy
@retry(
    retry_on_exception=lambda exc: isinstance(exc, Exception),  # Retry on any exception
    wait_fixed=1,  # Wait 1 second between retries
    stop_max_attempt_number=3,  # Maximum number of retry attempts
)
def create_customer_with_retry(
    customer_data: CustomerCreate,
    db: Session,
):
    new_customer = Customer(**customer_data)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


# Retrieve a list of all customers
@customer_router.get("/v1/customers", tags = ["customers"])
def get_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

# Retrieve a single customer's details by ID
@customer_router.get("/v1/customers/{customer_id}", tags = ["customers"])
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Update customer information
@customer_router.put("/v1/customers/{customer_id}", tags = ["customers"])
def update_customer(customer_id: int, customer_data: dict, db: Session = Depends(get_db)):
    existing_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for key, value in customer_data.items():
        setattr(existing_customer, key, value)
    
    db.commit()
    db.refresh(existing_customer)
    return existing_customer

# Delete a customer by ID
@customer_router.delete("/v1/customers/{customer_id}", tags = ["customers"])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    existing_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(existing_customer)
    db.commit()
    return {"message": "Customer deleted"}
