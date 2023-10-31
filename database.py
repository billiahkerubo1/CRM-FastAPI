from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#import psycopg2
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# conn = psycopg2.connect(database = "CRM", 
#                         user = "postgres", 
#                         host= 'localhost',
#                         password = 
#                         port = 5436)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()