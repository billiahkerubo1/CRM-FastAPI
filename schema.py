from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    tenant_id: int

    class Config:
        orm_mode = True

class TenantBase(BaseModel):
    name: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    tenant_id: int

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    tenant_id: int

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int

    class Config:
        orm_mode = True

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    customer_id: int
    tenant_id: int

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    contact_id: int

    class Config:
        orm_mode = True

class InteractionBase(BaseModel):
    interaction_type: str
    interaction_date: str
    notes: str
    customer_id: int
    contact_id: int
    tenant_id: int

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    interaction_id: int

    class Config:
        orm_mode = True

class DealBase(BaseModel):
    deal_name: str
    deal_stage: str
    deal_value: float
    customer_id: int
    tenant_id: int

class DealCreate(DealBase):
    pass

class Deal(DealBase):
    deal_id: int

    class Config:
        orm_mode = True
class Settings(BaseModel):
    authjwt_secret_key:str = 'f364aba27b04693a752cdd5777ae9e8db734ecc2ad8df063b5605398183a6db7'
class LoginModel(BaseModel):
    email:str
    password:str