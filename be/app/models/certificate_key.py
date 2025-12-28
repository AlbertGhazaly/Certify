from sqlalchemy import Column, String
from app.database.connection import Base

class CertificateKey(Base):
    __tablename__ = "certificate_keys"
    
    student_id = Column(String, primary_key=True, index=True)
    aes_key = Column(String, nullable=False)  # Base64 encoded AES key