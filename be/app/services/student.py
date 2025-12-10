import hashlib
import secrets
from typing import Optional
from sqlalchemy.orm import Session
from app.models.student import Student


class StudentService:
    """Service for managing student data"""
    
    @staticmethod
    def generate_unique_nonce() -> str:
        """Generate a unique nonce for student hash"""
        return secrets.token_hex(32)
    
    @staticmethod
    def generate_hash_val(nim: str, nama: str, unique_nonce: str) -> str:
        """
        Generate SHA-256 hash from NIM, Nama, and unique_nonce
        Hash_val = hash_sha256(NIM, Nama, unique_nonce)
        """
        data = f"{nim}{nama}{unique_nonce}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def create_student(
        db: Session,
        wallet_address: str,
        nim: str,
        nama: str
    ) -> Student:
        """
        Create a new student record with generated hash
        """
        # Generate unique nonce
        unique_nonce = StudentService.generate_unique_nonce()
        
        # Generate hash_val
        hash_val = StudentService.generate_hash_val(nim, nama, unique_nonce)
        
        # Create student record
        student = Student(
            id=wallet_address,
            hash_val=hash_val,
            nim=nim,
            nama=nama,
            unique_nonce=unique_nonce
        )
        
        db.add(student)
        db.commit()
        db.refresh(student)
        
        return student
    
    @staticmethod
    def get_student_by_wallet(db: Session, wallet_address: str) -> Optional[Student]:
        """Get student by wallet address"""
        return db.query(Student).filter(Student.id == wallet_address).first()
    
    @staticmethod
    def get_student_by_nim(db: Session, nim: str) -> Optional[Student]:
        """Get student by NIM"""
        return db.query(Student).filter(Student.nim == nim).first()
    
    @staticmethod
    def verify_student_hash(student: Student) -> bool:
        """Verify that the stored hash matches the computed hash"""
        computed_hash = StudentService.generate_hash_val(
            student.nim,
            student.nama,
            student.unique_nonce
        )
        return computed_hash == student.hash_val
    
    @staticmethod
    def delete_student(db: Session, wallet_address: str) -> bool:
        """Delete student by wallet address"""
        student = db.query(Student).filter(Student.id == wallet_address).first()
        if student:
            db.delete(student)
            db.commit()
            return True
        return False
