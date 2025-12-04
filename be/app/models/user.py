from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    publicKeyX = Column(String)
    publicKeyY = Column(String)