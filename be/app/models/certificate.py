from sqlalchemy import Column, String
from app.database.connection import Base

class Certificate(Base):
    """
    Certificate table
    Stores certificate encryption keys indexed by NIM
    """
    __tablename__ = "certificates"
    
    id = Column(String, primary_key=True, index=True, name="id")
    aes_key = Column(String, nullable=False)
