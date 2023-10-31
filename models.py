from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey,Numeric
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=False)

class Tenant(Base):
    __tablename__ = "tenants"
    
    tenant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone_number = Column(String(20))
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=False)
    
    # Define a relationship to interactions and deals
    interactions = relationship("Interaction", back_populates="customer")
    deals = relationship("Deal", back_populates="customer")

class Contact(Base):
    __tablename__ = "contacts"
    
    contact_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone_number = Column(String(20))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=False)
    
    # Define a relationship to interactions
    interactions = relationship("Interaction", back_populates="contact")

class Interaction(Base):
    __tablename__ = "interactions"
    
    interaction_id = Column(Integer, primary_key=True, index=True)
    interaction_type = Column(String(100), nullable=False)
    interaction_date = Column(DateTime, nullable=False)
    notes = Column(Text)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    contact_id = Column(Integer, ForeignKey("contacts.contact_id"))
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=False)
    
    # Define relationships to customers and contacts
    customer = relationship("Customer", back_populates="interactions")
    contact = relationship("Contact", back_populates="interactions")

class Deal(Base):
    __tablename__ = "deals"
    
    deal_id = Column(Integer, primary_key=True, index=True)
    deal_name = Column(String(255), nullable=False)
    deal_stage = Column(String(100))
    deal_value = Column(Numeric(12, 2))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=False)
    
    # Define a relationship to customers
    customer = relationship("Customer", back_populates="deals")
# Create the tables
engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)

# You can use a session to interact with the database
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = Session()