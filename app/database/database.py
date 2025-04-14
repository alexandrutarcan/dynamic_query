import os
from decimal import Decimal
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from app.database.db import SessionLocal

def serialize_value(value):
    if isinstance(value, Decimal):
        return float(value)
    return value

# Return tables structure as a string
def get_db_schema():
    engine = create_engine(os.getenv("DATABASE_URL"))
    try:
      print("Connecting to db to retrieve schema...")
      inspector = inspect(engine)
      tables = inspector.get_table_names()

      db_schema = ""
      for table in tables:
         if table in ["budgets","expenses","goals"]:
            db_schema += f"Schema for table {table}:\n"
            columns = inspector.get_columns(table)
            for column in columns:
                db_schema += f"  -{column['name']} ({column['type']})\n"
    except OperationalError as e:
        print(f"Database connection error: {e}")
        return "Database connection failed"
    return db_schema

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_query(db: Session, sql_query: str):
    try:
        result = db.execute(text(sql_query))
        rows = result.fetchall()

        # Convert each row to a dictionary for JSON-ready response
        data = [
            {key: serialize_value(value) for key, value in row._mapping.items()}
            for row in rows
        ]
        # print(f"Select result:\n{data}\n")

        return {
            "status": "success",
            "row_count": len(data),
            "data": data
        }

    except Exception as e:
        print(f"Error executing query: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

        

    