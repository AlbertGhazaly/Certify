from pydantic import BaseModel
from typing import Optional

class ChallengeRequest(BaseModel):
    wallet_address: str

class ChallengeResponse(BaseModel):
    challenge: str
    nonce: str

class VerifyRequest(BaseModel):
    wallet_address: str
    signature: str

class VerifyResponse(BaseModel):
    success: bool
    message: str
    session_token: Optional[str] = None
    jwt_token: Optional[str] = None
    role: Optional[str] = None
    wallet_address: Optional[str] = None

class LogoutRequest(BaseModel):
    wallet_address: str