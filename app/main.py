from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.db import Base, engine, SessionLocal
from app.database.user import User
from app.database.models import Budget, Expense, Goal
from app.database.populate_users import populate_users
from app.database.transaction import Transaction
from app.database.populate_transactions import populate_transactions
from app.database.populate_tables import populate_tables
from app.query_request import QueryRequest
from app.request_service import process_request
from app.database.database import get_db_schema
from app.database.database import get_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    #SQLAlchemy will:
        # Look for all classes that inherit from Base
        # Create the actual tables in your PostgreSQL DB
    Base.metadata.create_all(bind=engine)
    print(get_db_schema())

@app.post("/populate/tables")
def populate():
    populate_tables()
    return {"message": "Tables populated"}
@app.post("/populate/users")
def populate():
    populate_users()
    return {"message": "Users populated"}


@app.post("/populate/transactions")
def populate_txns():
    populate_transactions()
    return {"message": "Transactions populated"}

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/users")
def get_users(db: Session= Depends(get_db)):
    result = db.execute(text("SELECT * FROM users"))
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

@app.get("/users/{user_id}/transactions")
def get_users_transactions(user_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM transactions where payer_id = :user_id"),
    {"user_id": user_id}
    )
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

@app.post("/ask")
def get_response(query_request: QueryRequest, db: Session = Depends(get_db)):
    try:
        return process_request(query_request.user_prompt, db)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")