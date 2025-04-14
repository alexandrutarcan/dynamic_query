import pandas as pd
from app.database.db import Base, engine, SessionLocal
from app.database.user import User

def populate_users():
    session = SessionLocal()

    # Create the table if it doesn't exist
    Base.metadata.create_all(bind=engine)

    # Load the CSV
    df = pd.read_csv('resources/users.csv')

    for _, row in df.iterrows():
        user = User(id=row['id'], full_name=row['full_name'], email=row['email'])
        session.merge(user)

    # Commit the transaction and close session
    session.commit()
    session.close()

    print("CSV data inserted successfully!")
