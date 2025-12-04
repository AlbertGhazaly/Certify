from sqlalchemy import Column, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Nonce(Base):
    __tablename__ = "nonces"
    
    wallet_address = Column(String, primary_key=True, index=True)
    nonce = Column(String, nullable=False)
    expires_at = Column(BigInteger, nullable=False)  # Unix timestamp