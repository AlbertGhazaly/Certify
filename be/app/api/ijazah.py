from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.ijazah import IjazahCreate, IjazahResponse, IjazahUpdate
from app.services.ijazah import IjazahService
from app.services.student import StudentService

router = APIRouter()

# ==================== IJAZAH (CERTIFICATE) ENDPOINTS ====================

@router.post("/certificates", response_model=IjazahResponse, status_code=status.HTTP_201_CREATED)
async def create_certificate(
    ijazah_data: IjazahCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new certificate (Ijazah) record
    - If AES key is not provided, it will be auto-generated
    """
    # Check if student exists
    student = StudentService.get_student_by_nim(db, ijazah_data.nim)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student with this NIM not found. Create student record first."
        )
    
    # Check if certificate already exists
    existing_ijazah = IjazahService.get_ijazah_by_nim(db, ijazah_data.nim)
    if existing_ijazah:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate for this NIM already exists"
        )
    
    try:
        ijazah = IjazahService.create_ijazah(
            db=db,
            nim=ijazah_data.nim,
            aes_key=ijazah_data.aes_key
        )
        return ijazah
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create certificate: {str(e)}"
        )

@router.get("/certificates/{nim}", response_model=IjazahResponse)
async def get_certificate(
    nim: str,
    db: Session = Depends(get_db)
):
    """Get certificate by NIM"""
    ijazah = IjazahService.get_ijazah_by_nim(db, nim)
    if not ijazah:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    return ijazah

@router.put("/certificates", response_model=IjazahResponse)
async def update_certificate_key(
    update_data: IjazahUpdate,
    db: Session = Depends(get_db)
):
    """Update AES key for a certificate"""
    ijazah = IjazahService.update_aes_key(db, update_data.nim, update_data.aes_key)
    if not ijazah:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    return ijazah

@router.delete("/certificates/{nim}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certificate(
    nim: str,
    db: Session = Depends(get_db)
):
    """Delete certificate by NIM"""
    success = IjazahService.delete_ijazah(db, nim)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    return None
