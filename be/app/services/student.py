import hashlib
import secrets
from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.ijazah import Ijazah

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
    def get_student_by_wallet(db: Session, wallet_address: str) -> Student | None:
        """Get student by wallet address"""
        return db.query(Student).filter(Student.id == wallet_address).first()
    
    @staticmethod
    def get_student_by_nim(db: Session, nim: str) -> Student | None:
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


class IjazahService:
    """Service for managing certificate (ijazah) data"""
    
    @staticmethod
    def generate_aes_key() -> str:
        """Generate a random AES-256 key (32 bytes = 256 bits)"""
        return secrets.token_hex(32)  # Returns 64 hex characters = 32 bytes
    
    @staticmethod
    def create_ijazah(db: Session, nim: str, aes_key: str = None) -> Ijazah:
        """
        Create a new certificate record
        If aes_key is not provided, a random one will be generated
        """
        if aes_key is None:
            aes_key = IjazahService.generate_aes_key()
        
        ijazah = Ijazah(
            id=nim,
            aes_key=aes_key
        )
        
        db.add(ijazah)
        db.commit()
        db.refresh(ijazah)
        
        return ijazah
    
    @staticmethod
    def get_ijazah_by_nim(db: Session, nim: str) -> Ijazah | None:
        """Get certificate by NIM"""
        return db.query(Ijazah).filter(Ijazah.id == nim).first()
    
    @staticmethod
    def update_aes_key(db: Session, nim: str, new_aes_key: str) -> Ijazah | None:
        """Update AES key for a certificate"""
        ijazah = db.query(Ijazah).filter(Ijazah.id == nim).first()
        if ijazah:
            ijazah.aes_key = new_aes_key
            db.commit()
            db.refresh(ijazah)
        return ijazah
    
    @staticmethod
    def delete_ijazah(db: Session, nim: str) -> bool:
        """Delete certificate by NIM"""
        ijazah = db.query(Ijazah).filter(Ijazah.id == nim).first()
        if ijazah:
            db.delete(ijazah)
            db.commit()
            return True
        return False
