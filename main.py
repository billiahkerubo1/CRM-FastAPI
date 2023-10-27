# main.py
import uvicorn
from contact import router
from customer import customer_router
from interactions import interact_router
from deal import deal_router
from fastapi import FastAPI
from app.database import engine
from app import models
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to your CRM API"}
# Include routers from different modules
# app.include_router(customer.router, prefix="/api")
# app.include_router(deal.router, prefix="/api")
# app.include_router(interaction.router, prefix="/api")
# app.include_router(contact.router, prefix="/api")
# app.include_router(auth.router, prefix="/api")
app.include_router(router,)
app.include_router(customer_router,)
app.include_router(interact_router,)
app.include_router(deal_router,)
if __name__ == "__main__":
    # Create database tables
    #Base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", port=9000, reload=True)