from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentVerify, StudentListResponse
from app.services.student import StudentService

router = APIRouter()

# ==================== STUDENT ENDPOINTS ====================

@router.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new student record
    - Generates unique_nonce automatically
    - Calculates hash_val = SHA256(NIM + Nama + unique_nonce)
    """
    # Check if student with this wallet address already exists
    existing_student = StudentService.get_student_by_wallet(db, student_data.wallet_address)
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this wallet address already exists"
        )
    
    # Check if student with this NIM already exists
    existing_nim = StudentService.get_student_by_nim(db, student_data.nim)
    if existing_nim:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this NIM already exists"
        )
    
    try:
        student = StudentService.create_student(
            db=db,
            wallet_address=student_data.wallet_address,
            nim=student_data.nim,
            nama=student_data.nama
        )
        return student
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create student: {str(e)}"
        )

@router.get("/students", response_model=list[StudentListResponse])
async def get_all_students(
    db: Session = Depends(get_db)
):
    """Get all students with only NIM, nama, and wallet address"""
    students = StudentService.get_all_students(db)
    return students

@router.get("/students/wallet/{wallet_address}", response_model=StudentResponse)
async def get_student_by_wallet(
    wallet_address: str,
    db: Session = Depends(get_db)
):
    """Get student information by wallet address"""
    student = StudentService.get_student_by_wallet(db, wallet_address)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.get("/students/nim/{nim}", response_model=StudentResponse)
async def get_student_by_nim(
    nim: str,
    db: Session = Depends(get_db)
):
    """Get student information by NIM"""
    student = StudentService.get_student_by_nim(db, nim)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.post("/students/verify")
async def verify_student_hash(
    verify_data: StudentVerify,
    db: Session = Depends(get_db)
):
    """
    Verify that a student's hash is valid
    Recalculates the hash and compares with stored hash_val
    """
    student = StudentService.get_student_by_wallet(db, verify_data.wallet_address)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Verify NIM and Nama match
    if student.nim != verify_data.nim or student.nama != verify_data.nama:
        return {
            "valid": False,
            "message": "Student data mismatch"
        }
    
    # Verify hash
    is_valid = StudentService.verify_student_hash(student)
    
    return {
        "valid": is_valid,
        "message": "Hash verification successful" if is_valid else "Hash verification failed"
    }

@router.delete("/students/{wallet_address}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    wallet_address: str,
    db: Session = Depends(get_db)
):
    """Delete student by wallet address"""
    success = StudentService.delete_student(db, wallet_address)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return None
