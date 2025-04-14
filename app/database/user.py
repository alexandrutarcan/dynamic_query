from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.db import Base
# Define the User model
# Base is a special SQLAlchemy class
# Created by calling declarative_base()
# It connects Python class to SQLAlchemy's ORM system.
# Any class that inherits from Base becomes a mapped class — SQLAlchemy knows it represents a table.

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    
    #They form a two-way connection between User and Transaction
    transactions = relationship("Transaction", back_populates="user")