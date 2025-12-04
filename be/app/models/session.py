from sqlalchemy import Column, String, BigInteger
from app.database.connection import Base

class Session(Base):
    __tablename__ = "sessions"
    
    wallet_address = Column(String, primary_key=True, index=True)
    public_key_x = Column(String, nullable=False)
    public_key_y = Column(String, nullable=False)
    created_at = Column(BigInteger, nullable=False)