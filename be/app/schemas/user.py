from pydantic import BaseModel

class UserBase(BaseModel):
    role: str
    username: str
    publicKeyX: str
    publicKeyY: str

    class Config:
        from_attributes = True  # Use this for Pydantic v2 compatibility

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int