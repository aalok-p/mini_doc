from pydantic import BaseModel, EmailStr, ConfigDict

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    phone: str | None
