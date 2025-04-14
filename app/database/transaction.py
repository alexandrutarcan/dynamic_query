from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_method_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(String, nullable=False)
    # timestamp = Column(DateTime, default=datetime.now)
    
    #Form a two-way connection between User and Transaction
    user = relationship("User", back_populates="transactions")
