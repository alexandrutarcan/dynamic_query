from sqlalchemy import Column, Integer, String, Text, Boolean, Date, Numeric, CheckConstraint
from app.database.db import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)
    date = Column(Date, nullable=False)
    payment_method = Column(String(30))
    is_recurring = Column(Boolean, default=False)

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    budget_amount = Column(Numeric(10, 2), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("budget_amount >= 0", name="check_budget_positive"),
        CheckConstraint("month BETWEEN 1 AND 12", name="check_valid_month"),
        CheckConstraint("year >= 2000", name="check_valid_year"),
    )

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    target_amount = Column(Numeric(10, 2), nullable=False)
    current_amount = Column(Numeric(10, 2), default=0)
    deadline = Column(Date)
    priority = Column(Integer)

    __table_args__ = (
        CheckConstraint("target_amount > 0", name="check_target_positive"),
        CheckConstraint("current_amount >= 0", name="check_current_nonnegative"),
        CheckConstraint("priority BETWEEN 1 AND 5", name="check_valid_priority"),
    )
