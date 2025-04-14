import pandas as pd
from app.database.transaction import Transaction
from app.database.db import SessionLocal

def populate_transactions():
    
    session = SessionLocal()

    df = pd.read_csv('resources/transactions.csv')

    for _, row in df.iterrows():
        txn = Transaction(
            id=row["id"],
            payer_id=row["payer_id"],
            payment_method_id=row["payment_method_id"],
            amount=row["amount"],
            currency=row["currency"],
            status=row["status"],
            description=row["description"]
        )
        session.merge(txn)

    session.commit()
    session.close()

    print("Transaction CSV data inserted successfully!")
