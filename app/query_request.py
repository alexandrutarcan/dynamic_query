from pydantic import BaseModel

class QueryRequest(BaseModel):
    user_prompt: str