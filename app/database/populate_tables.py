import pandas as pd
from app.database.db import Base, engine, SessionLocal
from app.database.models import Budget, Expense, Goal

def populate_tables():
    session = SessionLocal()

    # Create the table if it doesn't exist
    Base.metadata.create_all(bind=engine)

    # Load the CSV
    df = pd.read_csv('resources/budgets.csv')

    for _, row in df.iterrows():
        budget = Budget(
         id=row['id'],
         category=row['category'],
         budget_amount=row['budget_amount'],
         month=row['month'],
         year=row['year']
        )
        session.merge(budget)
    
    # Load the CSV
    df = pd.read_csv('resources/expenses.csv')

    for _, row in df.iterrows():
        expense = Expense(
        id=row['id'],
        amount=row['amount'],
        category=row['category'],
        description=row.get('description'),
        date=row['date'],
        payment_method=row.get('payment_method'),
        is_recurring=row.get('is_recurring', False)
        )
        session.merge(expense)

    # Load the CSV
    df = pd.read_csv('resources/goals.csv')

    for _, row in df.iterrows():
        goal = Goal(
        id=row['id'],
        name=row['name'],
        target_amount=row['target_amount'],
        current_amount=row['current_amount'],
        deadline=row['deadline'],
        priority=row['priority']
        )
        session.merge(goal)

    # Commit the transaction and close session
    session.commit()
    session.close()

    print("CSV data inserted successfully!")
