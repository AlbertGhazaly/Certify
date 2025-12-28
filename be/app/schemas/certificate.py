from pydantic import BaseModel
from typing import Optional, List

class IssueCertificateRequest(BaseModel):
    student_name: str
    student_id: str
    degree: str
    birth_place: str
    birth_date: str
    issue_date: str
    issuer_wallets: List[str]  # List of issuer addresses
    requires_all_signatures: bool = True

class IssueCertificateResponse(BaseModel):
    success: bool
    message: str
    student_id: Optional[str] = None
    ipfs_cid: Optional[str] = None
    cert_hash: Optional[str] = None
    aes_key: Optional[str] = None  # Return key only once

class VerifyCertificateRequest(BaseModel):
    student_id: str
    aes_key: str  # User provides key to decrypt

class VerifyCertificateResponse(BaseModel):
    success: bool
    valid: bool
    certificate_text: Optional[str] = None
    ipfs_cid: Optional[str] = None
    message: str