from sqlalchemy import Column, String
from app.database.connection import Base

class Student(Base):
    """
    Student_list table
    Stores student information with wallet address as primary key
    """
    __tablename__ = "student_list"
    
    # Id = wallet_address (primary key)
    id = Column(String, primary_key=True, index=True, name="id")
    
    # Hash_val = hash_sha256(NIM, Nama, unique_nonce)
    hash_val = Column(String, nullable=False, unique=True)
    
    # NIM (Student ID Number)
    nim = Column(String, nullable=False, index=True)
    
    # Nama (Name)
    nama = Column(String, nullable=False)
    
    # unique_nonce used for hash generation
    unique_nonce = Column(String, nullable=False)
