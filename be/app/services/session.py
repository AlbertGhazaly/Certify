from sqlalchemy.orm import Session as DBSession
from app.models.session import Session
from typing import Optional  # Add this import for older Python versions
import time

class SessionService:
    @staticmethod
    def create_session(db: DBSession, wallet_address: str, public_key_x: str, public_key_y: str) -> Session:
        """Create session for authenticated user"""
        # Check if session exists
        db_session = db.query(Session).filter(Session.wallet_address == wallet_address).first()
        
        if db_session:
            db_session.public_key_x = public_key_x
            db_session.public_key_y = public_key_y
            db_session.created_at = int(time.time())
        else:
            db_session = Session(
                wallet_address=wallet_address,
                public_key_x=public_key_x,
                public_key_y=public_key_y,
                created_at=int(time.time())
            )
            db.add(db_session)
        
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def get_session(db: DBSession, wallet_address: str) -> Optional[Session]:  # Use Optional for compatibility
        """Get session for wallet address"""
        return db.query(Session).filter(Session.wallet_address == wallet_address).first()
    
    @staticmethod
    def delete_session(db: DBSession, wallet_address: str) -> bool:
        """Delete session on logout"""
        db_session = db.query(Session).filter(Session.wallet_address == wallet_address).first()
        if db_session:
            db.delete(db_session)
            db.commit()
            return True
        return False