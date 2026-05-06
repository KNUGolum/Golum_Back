from pydantic import BaseModel, EmailStr

class EmailCheckRequest(BaseModel):
    email: EmailStr

class NicknameCheckRequest(BaseModel):
    nickname: str

class UserCreate(BaseModel):
    email: EmailStr
    nickname: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    credit: int
    
    class Config:
        from_attributes = True