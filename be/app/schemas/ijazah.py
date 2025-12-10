from typing import Optional
from pydantic import BaseModel, Field

class IjazahBase(BaseModel):
    """Base schema for Ijazah (Certificate)"""
    nim: str = Field(..., description="Student ID Number (NIM) - primary key")

class IjazahCreate(IjazahBase):
    """Schema for creating a new certificate"""
    aes_key: Optional[str] = Field(None, description="AES encryption key (auto-generated if not provided)")

class IjazahResponse(IjazahBase):
    """Schema for certificate response"""
    id: str = Field(..., description="NIM (ID)")
    aes_key: str = Field(..., description="AES encryption key")
    
    class Config:
        from_attributes = True

class IjazahUpdate(BaseModel):
    """Schema for updating certificate AES key"""
    nim: str
    aes_key: str = Field(..., description="New AES encryption key")