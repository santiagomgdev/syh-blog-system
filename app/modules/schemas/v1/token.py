from pydantic import BaseModel, EmailStr

class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    refresh_token: str

# app/schemas/user.py (extensión)
class UserLogin(BaseModel):
    email: EmailStr
    password: str