from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.certificate import CertificateCreate, CertificateResponse, CertificateUpdate
from app.services.certificate import CertificateService
from app.services.student import StudentService
from app.services.read_contract import ContractService

router = APIRouter()
contract_service = ContractService()

# ==================== CERTIFICATE ENDPOINTS ====================

@router.post("/certificates", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
async def create_certificate(
    certificate_data: CertificateCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new certificate record
    - If AES key is not provided, it will be auto-generated
    """
    # Check if student exists
    student = StudentService.get_student_by_nim(db, certificate_data.nim)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student with this NIM not found. Create student record first."
        )
    
    # Check if certificate already exists
    existing_certificate = CertificateService.get_certificate_by_nim(db, certificate_data.nim)
    if existing_certificate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate for this NIM already exists"
        )
    
    try:
        certificate = CertificateService.create_certificate(
            db=db,
            nim=certificate_data.nim,
            aes_key=certificate_data.aes_key
        )
        return certificate
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create certificate: {str(e)}"
        )

@router.get("/certificates/{nim}", response_model=CertificateResponse)
async def get_certificate(
    nim: str,
    db: Session = Depends(get_db)
):
    """Get certificate by NIM"""
    certificate = CertificateService.get_certificate_by_nim(db, nim)
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    return certificate

@router.put("/certificates", response_model=CertificateResponse)
async def update_certificate_key(
    update_data: CertificateUpdate,
    db: Session = Depends(get_db)
):
    """Update AES key for a certificate"""
    certificate = CertificateService.update_aes_key(db, update_data.nim, update_data.aes_key)
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    return certificate

@router.delete("/certificates/{nim}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certificate(
    nim: str,
    db: Session = Depends(get_db)
):
    """Delete certificate by NIM"""
    success = CertificateService.delete_certificate(db, nim)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    return None

@router.get("/certificates/blockchain/all")
async def get_all_certificates_from_blockchain():
    """Get all certificates from blockchain smart contract"""
    try:
        certificates = contract_service.get_all_certificates()
        return {
            "success": True,
            "certificates": certificates,
            "count": len(certificates)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch certificates from blockchain: {str(e)}"
        )
