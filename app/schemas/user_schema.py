from typing import Optional
from pydantic import BaseModel
    
# --------------------
# User Schemas
# --------------------
class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str
    admin_secret: Optional[str] = None  # <-- new optional field for admin creation

class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: str
    role: str  # <-- add this


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
