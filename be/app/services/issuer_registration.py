from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, asc, desc
from datetime import datetime

from app.models.Issuer_registration import Issuer_registration, IssuerStatus
from app.services.session import (
    SessionService
)

class IssuerRegistrationService:
    """Service for managing issuer registrations"""

    @staticmethod
    def create_registration(
        db: Session,
        name: str,
        wallet_address: str,
        created_at: Optional[int] = None,
    ) -> Issuer_registration:
        """Create new issuer registration (default status: pending)"""

        if created_at is None:
            created_at = int(datetime.utcnow().timestamp())
        session = SessionService.get_session(db, wallet_address)
        if not session:
            raise Exception("No active session found for the given wallet address.")
        registration = Issuer_registration(
            name=name,
            wallet_address=wallet_address,
            public_key_x=session.public_key_x,
            public_key_y=session.public_key_y,
            created_at=created_at,
            status=IssuerStatus.pending,
        )

        db.add(registration)
        db.commit()
        db.refresh(registration)

        return registration

    @staticmethod
    def get_by_id(
        db: Session, id_registration: str
    ) -> Optional[Issuer_registration]:
        return (
            db.query(Issuer_registration)
            .filter(Issuer_registration.id_registration == id_registration)
            .first()
        )
    
    @staticmethod
    def get_by_wallet(
        db: Session, wallet_address: str
    ) -> Optional[Issuer_registration]:
        return (
            db.query(Issuer_registration)
            .filter(Issuer_registration.wallet_address == wallet_address)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        name: Optional[str] = None,
        status: Optional[IssuerStatus] = None,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        sort: str = "latest",
        page: int = 1,
        page_size: int = 10,
    ) -> dict:
        """
        Get all registrations with filters + pagination
        """

        query = db.query(Issuer_registration)

        # Filters
        if name:
            query = query.filter(Issuer_registration.name.ilike(f"%{name}%"))

        if status:
            query = query.filter(Issuer_registration.status == status)

        if start_date:
            query = query.filter(Issuer_registration.created_at >= start_date)

        if end_date:
            query = query.filter(Issuer_registration.created_at <= end_date)

        # Sorting
        if sort == "oldest":
            query = query.order_by(asc(Issuer_registration.created_at))
        else:
            query = query.order_by(desc(Issuer_registration.created_at))
        
        total = query.count()

        # Pagination
        offset = (page - 1) * page_size
        items = (
            query.order_by(Issuer_registration.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }

    @staticmethod
    def update_status(
        db: Session,
        id_registration: str,
        status: IssuerStatus,
    ) -> Optional[Issuer_registration]:
        """Accept or reject issuer registration"""

        registration = (
            db.query(Issuer_registration)
            .filter(Issuer_registration.id_registration == id_registration)
            .first()
        )

        if not registration:
            return None

        registration.status = status
        db.commit()
        db.refresh(registration)

        return registration

    @staticmethod
    def accept_registration(db: Session, id_registration: str):
        return IssuerRegistrationService.update_status(
            db, id_registration, IssuerStatus.accept
        )

    @staticmethod
    def reject_registration(db: Session, id_registration: str):
        return IssuerRegistrationService.update_status(
            db, id_registration, IssuerStatus.reject
        )

    @staticmethod
    def delete_registration(
        db: Session, id_registration: str
    ) -> bool:
        registration = (
            db.query(Issuer_registration)
            .filter(Issuer_registration.id_registration == id_registration)
            .first()
        )

        if not registration:
            return False

        db.delete(registration)
        db.commit()
        return True
