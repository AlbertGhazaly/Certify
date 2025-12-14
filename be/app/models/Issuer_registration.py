from sqlalchemy import Column, String, BigInteger, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database.connection import Base
import enum
import uuid


class IssuerStatus(enum.Enum):
    accept = "accept"
    reject = "reject"
    pending = "pending"

class Issuer_registration(Base):
    __tablename__ = "issuer_registration"

    id_registration = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    wallet_address = Column(String, nullable=False, unique=True, index=True)
    public_key_x = Column(String, nullable=False)
    public_key_y = Column(String, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    status = Column(Enum(IssuerStatus), nullable=False, default=IssuerStatus.pending)