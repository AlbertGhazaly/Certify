from sqlalchemy.orm import Session as DBSession
from app.models.session import Session
from typing import Optional
import time
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

class SessionService:
    @staticmethod
    def create_jwt_token(wallet_address: str, role: str) -> str:
        """Create JWT token for authenticated user"""
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        to_encode = {
            "wallet_address": wallet_address,
            "role": role,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_jwt_token(token: str) -> Optional[dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def create_session(
        db: DBSession, 
        wallet_address: str, 
        public_key_x: str, 
        public_key_y: str,
        role: str,
        jwt_token: str
    ) -> Session:
        """Create session for authenticated issuer"""
        # Check if session exists
        db_session = db.query(Session).filter(Session.wallet_address == wallet_address).first()
        
        if db_session:
            # Update existing session
            db_session.public_key_x = public_key_x
            db_session.public_key_y = public_key_y
            db_session.role = role
            db_session.jwt_token = jwt_token
            db_session.created_at = int(time.time())
        else:
            # Create new session
            db_session = Session(
                wallet_address=wallet_address,
                public_key_x=public_key_x,
                public_key_y=public_key_y,
                role=role,
                jwt_token=jwt_token,
                created_at=int(time.time())
            )
            db.add(db_session)
        
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def get_session(db: DBSession, wallet_address: str) -> Optional[Session]:
        """Get session for wallet address"""
        return db.query(Session).filter(Session.wallet_address == wallet_address).first()
    
    @staticmethod
    def get_session_by_token(db: DBSession, token: str) -> Optional[Session]:
        """Get session by JWT token"""
        return db.query(Session).filter(Session.jwt_token == token).first()
    
    @staticmethod
    def delete_session(db: DBSession, wallet_address: str) -> bool:
        """Delete session on logout"""
        db_session = db.query(Session).filter(Session.wallet_address == wallet_address).first()
        if db_session:
            db.delete(db_session)
            db.commit()
            return True
        return False
    
    @staticmethod
    def validate_session_token(db: DBSession, token: str) -> Optional[Session]:
        """Validate JWT token and return session"""
        payload = SessionService.verify_jwt_token(token)
        if not payload:
            return None
        
        wallet_address = payload.get("wallet_address")
        if not wallet_address:
            return None
        
        session = SessionService.get_session(db, wallet_address)
        if session and session.jwt_token == token:
            return session
        
        return None