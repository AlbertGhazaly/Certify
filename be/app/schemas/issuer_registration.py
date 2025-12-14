from typing import List
from pydantic import BaseModel
from app.models.Issuer_registration import IssuerStatus
from uuid import UUID

class IssuerRegistrationCreate(BaseModel):
    name: str
    wallet_address: str
    # public_key_x: str
    # public_key_y: str


class IssuerRegistrationResponse(BaseModel):
    id_registration: UUID
    name: str
    wallet_address: str
    public_key_x: str
    public_key_y: str
    created_at: int
    status: IssuerStatus

    class Config:
        from_attributes = True


class IssuerRegistrationListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[IssuerRegistrationResponse]
