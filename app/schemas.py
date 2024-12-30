from pydantic import BaseModel

class TermCreate(BaseModel):
    name: str
    description: str

class TermResponse(BaseModel):
    id: int
    name: str
    description: str
