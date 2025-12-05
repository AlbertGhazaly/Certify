from sqlalchemy import Column, String, ForeignKey
from app.database.connection import Base

class Ijazah(Base):
    """
    Ijazah (Certificate) table
    Stores certificate encryption keys indexed by NIM
    """
    __tablename__ = "ijazah"
    
    # Id: NIM (primary key)
    id = Column(String, primary_key=True, index=True, name="id")
    
    # AES_Key for certificate encryption
    aes_key = Column(String, nullable=False)
