# contact.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Contact, Customer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the desired log level
logger = logging.getLogger(__name__)  # Create a logger

# Define a custom log format
log_formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] - %(message)s")

# Create a file handler to log to a file
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Optionally,  create a stream handler to log to the console
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

router = APIRouter()

# Create a new contact for a customer
@router.post("/contact/{customer_id}", tags = ["contacts"])
def create_contact_for_customer(customer_id: int, contact_data: dict, db: Session = Depends(get_db)):
    # Check if the customer exists
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    new_contact = Contact(**contact_data, customer_id=customer_id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

# Retrieve a list of all contacts
#@router.get("/contacts")
#def get_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
 #   contacts = db.query(Contact).offset(skip).limit(limit).all()
  #  return contacts

# Retrieve a single contact's details by ID
@router.get("/contacts/{contact_id}", tags = ["contacts"])
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Update contact information
@router.put("/contacts/{contact_id}", tags = ["contacts"])
def update_contact(contact_id: int, contact_data: dict, db: Session = Depends(get_db)):
    existing_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if existing_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for key, value in contact_data.items():
        setattr(existing_contact, key, value)
    
    db.commit()
    db.refresh(existing_contact)
    return existing_contact

# Delete a contact by ID
@router.delete("/contact/{contact_id}", tags = ["contacts"])
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    existing_contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if existing_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(existing_contact)
    db.commit()
    logger.info("Request to delete contact")
    return {"message": "Contact deleted"}
