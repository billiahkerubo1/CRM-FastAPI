# interaction.py
from fastapi import APIRouter, Depends, HTTPException
#from app.database import conn
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Interaction

interact_router = APIRouter()

# Log a new interaction
@interact_router.post("/interaction", tags = ["interactions"])
def log_interaction(interaction_data: dict, db: Session = Depends(get_db)):
    new_interaction = Interaction(**interaction_data)
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    return new_interaction

# Retrieve a list of interactions for a customer or contact
@interact_router.get("/interactions", tags = ["interactions"])
def get_interactions(target_id: int, target_type: str, db: Session = Depends(get_db)):
    # Target type can be "customer" or "contact"
    if target_type not in ["customer", "contact"]:
        raise HTTPException(status_code=400, detail="Invalid target type")
    
    interactions = db.query(Interaction).filter(getattr(Interaction, f"{target_type}_id") == target_id).all()
    return interactions

# Update an interaction
@interact_router.put("/interaction/{interaction_id}", tags = ["interactions"])
def update_interaction(interaction_id: int, interaction_data: dict, db: Session = Depends(get_db)):
    existing_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if existing_interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    for key, value in interaction_data.items():
        setattr(existing_interaction, key, value)
    
    db.commit()
    db.refresh(existing_interaction)
    return existing_interaction

# Delete an interaction
@interact_router.delete("/interaction/{interaction_id}", tags = ["interactions"])
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    existing_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if existing_interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    db.delete(existing_interaction)
    db.commit()
    return {"message": "Interaction deleted"}
