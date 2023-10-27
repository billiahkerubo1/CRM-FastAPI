# deal.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Deal

deal_router = APIRouter()

# Create a new deal/opportunity
@deal_router.post("/deal", tags = ["deals"])
def create_deal(deal_data: dict, db: Session = Depends(get_db)):
    new_deal = Deal(**deal_data)
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    return new_deal

# Retrieve a list of all deals
@deal_router.get("/deals", tags = ["deals"])
def get_deals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    deals = db.query(Deal).offset(skip).limit(limit).all()
    return deals

# Retrieve a single deal's details by ID
@deal_router.get("/deal/{deal_id}", tags = ["deals"])
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal

# Update deal information
@deal_router.put("/deal/{deal_id}", tags = ["deals"])
def update_deal(deal_id: int, deal_data: dict, db: Session = Depends(get_db)):
    existing_deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if existing_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    for key, value in deal_data.items():
        setattr(existing_deal, key, value)
    
    db.commit()
    db.refresh(existing_deal)
    return existing_deal

# Delete a deal by ID
@deal_router.delete("/deal/{deal_id}", tags = ["deals"])
def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    existing_deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if existing_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    db.delete(existing_deal)
    db.commit()
    return {"message": "Deal deleted"}
