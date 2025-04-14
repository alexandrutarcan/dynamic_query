import os
import json
from sqlalchemy import text
from openai import OpenAI
from fastapi import HTTPException
from app.database.database import get_db, execute_query
from app.prompts import ROLE_PROMPT, VALIDATION_PROMPT, NARRATIVE_PROMPT


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"

#checks if a sql query is valid before execution
def validate_sql(sql_query:str):
    
    # Validate sql query using a model
    validation_result = submit_ai_request(MODEL, system_instructions= VALIDATION_PROMPT, user_instructions= sql_query)
    print(f"Validation result:{validation_result}\n")
    if "!FAILED!" in validation_result:
        return False
    
    # If model passes, perform a PostgreSql Validation
    db = next(get_db())
    try:
        print(f"Passed AI validation.\nPerforming PostgreSQL validation...")
        db.execute(text(f"Explain {sql_query}"))
        return True
    except Exception as e:
        return False
    

def process_request(user_prompt:str, db):
    # Generate a SQL query using request to a model
    sql_query =  submit_ai_request(MODEL,system_instructions = ROLE_PROMPT, user_instructions= user_prompt)
    print(f"Generated SQL Query: {sql_query}")

    is_valid = validate_sql(sql_query)
    if not is_valid:
        raise HTTPException(status_code = 400)
    
    # Execute sql query
    query_results = execute_query(db, sql_query)

    # Convert the query result (dict) to a JSON string for GPT
    json_data_str = json.dumps(query_results, indent=2)
    print(f"Query Results in JSON Format:\n{json_data_str}")

    narrated_response = submit_ai_request(MODEL, system_instructions= NARRATIVE_PROMPT, user_instructions=json_data_str)
    return narrated_response

def submit_ai_request(model, system_instructions, user_instructions):
    client = OpenAI(api_key=OPENAI_API_KEY)  

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_instructions}
        ]
    )

    return response.choices[0].message.content.strip()