from typing import Optional
from sqlalchemy.orm import Session
import secrets
from app.models.ijazah import Ijazah

class IjazahService:
    """Service for managing certificate (ijazah) data"""
    
    @staticmethod
    def generate_aes_key() -> str:
        """Generate a random AES-256 key (32 bytes = 256 bits)"""
        return secrets.token_hex(32)  # Returns 64 hex characters = 32 bytes
    
    @staticmethod
    def create_ijazah(db: Session, nim: str, aes_key: Optional[str] = None) -> Ijazah:
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
    def get_ijazah_by_nim(db: Session, nim: str) -> Optional[Ijazah]:
        """Get certificate by NIM"""
        return db.query(Ijazah).filter(Ijazah.id == nim).first()
    
    @staticmethod
    def update_aes_key(db: Session, nim: str, new_aes_key: str) -> Optional[Ijazah]:
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