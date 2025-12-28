from pydantic import BaseModel
from typing import Optional, List

class IssueCertificateRequest(BaseModel):
    student_name: str
    student_id: str
    degree: str
    birth_place: str
    birth_date: str
    issue_date: str
    issuer_wallets: List[str]
    requires_all_signatures: bool = True

class IssueCertificateResponse(BaseModel):
    success: bool
    message: str
    student_id: Optional[str] = None
    ipfs_cid: Optional[str] = None
    cert_hash: Optional[str] = None
    aes_key: Optional[str] = None

class VerifyCertificateRequest(BaseModel):
    student_id: str

class VerifyCertificateResponse(BaseModel):
    success: bool
    valid: bool
    message: str
    certificate_text: Optional[str] = None
    ipfs_cid: Optional[str] = None
    file_url: Optional[str] = None

class PublicVerifyRequest(BaseModel):
    ipfs_cid: str
    aes_key: str
    cert_hash: str

class PublicVerifyResponse(BaseModel):
    success: bool
    valid: bool
    message: str
    certificate_text: Optional[str] = None
    file_url: Optional[str] = None

class SignCertificateRequest(BaseModel):
    student_id: str

class SignCertificateResponse(BaseModel):
    success: bool
    message: str
    student_id: Optional[str] = None
    cert_hash: Optional[str] = None
    ipfs_cid: Optional[str] = None
    certificate_data: Optional[dict] = None