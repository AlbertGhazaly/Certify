from pydantic import BaseModel

class UserBase(BaseModel):
    role: str
    username: str
    publicKeyX: str
    publicKeyY: str

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int