from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    """Base schema for Student"""
    nim: str = Field(..., description="Student ID Number (NIM)")
    nama: str = Field(..., description="Student Name")

class StudentCreate(StudentBase):
    """Schema for creating a new student"""
    wallet_address: str = Field(..., description="Wallet address (will be used as ID)")

class StudentResponse(StudentBase):
    """Schema for student response"""
    id: str = Field(..., description="Wallet address (ID)")
    hash_val: str = Field(..., description="SHA-256 hash of NIM, Nama, and unique_nonce")
    unique_nonce: str = Field(..., description="Unique nonce used in hash generation")
    
    class Config:
        from_attributes = True

class StudentVerify(BaseModel):
    """Schema for verifying student hash"""
    wallet_address: str
    nim: str
    nama: str

class StudentListResponse(BaseModel):
    """Schema for student list response - minimal info"""
    nim: str = Field(..., description="Student ID Number (NIM)")
    nama: str = Field(..., description="Student Name")
    wallet_address: str = Field(..., description="Wallet address")
    
    class Config:
        from_attributes = True



