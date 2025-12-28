from sqlalchemy import Column, String
from app.database.connection import Base

class Student(Base):
    """
    Student_list table
    Stores student information with wallet address as primary key
    """
    __tablename__ = "student_list"
    
    id = Column(String, primary_key=True, index=True, name="id")
    hash_val = Column(String, nullable=False, unique=True)
    nim = Column(String, nullable=False, index=True)
    nama = Column(String, nullable=False)
    unique_nonce = Column(String, nullable=False)
