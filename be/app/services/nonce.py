from sqlalchemy.orm import Session
from app.models.nonce import Nonce
from typing import Optional  # Add this import for older Python versions
import time

class NonceService:
    NONCE_EXPIRY_SECONDS = 300  # 5 minutes
    
    @staticmethod
    def create_nonce(db: Session, wallet_address: str, nonce: str) -> Nonce:
        """Create or update nonce for wallet address"""
        expires_at = int(time.time()) + NonceService.NONCE_EXPIRY_SECONDS
        
        # Check if nonce exists
        db_nonce = db.query(Nonce).filter(Nonce.wallet_address == wallet_address).first()
        
        if db_nonce:
            db_nonce.nonce = nonce
            db_nonce.expires_at = expires_at
        else:
            db_nonce = Nonce(
                wallet_address=wallet_address,
                nonce=nonce,
                expires_at=expires_at
            )
            db.add(db_nonce)
        
        db.commit()
        db.refresh(db_nonce)
        return db_nonce
    
    @staticmethod
    def get_nonce(db: Session, wallet_address: str) -> Optional[Nonce]:  # Use Optional for compatibility
        """Get nonce for wallet address if not expired"""
        db_nonce = db.query(Nonce).filter(Nonce.wallet_address == wallet_address).first()
        
        if db_nonce and db_nonce.expires_at > int(time.time()):
            return db_nonce
        
        # Clean up expired nonce
        if db_nonce:
            db.delete(db_nonce)
            db.commit()
        
        return None
    
    @staticmethod
    def delete_nonce(db: Session, wallet_address: str) -> None:
        """Delete nonce after successful verification"""
        db_nonce = db.query(Nonce).filter(Nonce.wallet_address == wallet_address).first()
        if db_nonce:
            db.delete(db_nonce)
            db.commit()
    
    @staticmethod
    def cleanup_expired_nonces(db: Session) -> int:
        """Clean up all expired nonces - can be run periodically"""
        current_time = int(time.time())
        deleted = db.query(Nonce).filter(Nonce.expires_at < current_time).delete()
        db.commit()
        return deleted