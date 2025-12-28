from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.issuer_registration import IssuerRegistrationService
from app.models.Issuer_registration import IssuerStatus
from app.schemas.issuer_registration import (
    IssuerRegistrationCreate,
    IssuerRegistrationResponse,
    IssuerRegistrationListResponse,
)

router = APIRouter()

@router.post(
    "/issuer-registrations",
    response_model=IssuerRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_registration(
    data: IssuerRegistrationCreate,
    db: Session = Depends(get_db),
):
    existing_registration = IssuerRegistrationService.get_by_wallet(
        db, data.wallet_address
    )
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Issuer registration with this wallet address already exists",
        )
    try:
        return IssuerRegistrationService.create_registration(
            db=db,
            name=data.name,
            wallet_address=data.wallet_address,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get(
    "/issuer-registrations/{id_registration}",
    response_model=IssuerRegistrationResponse,
)
def get_registration(
    id_registration: str,
    db: Session = Depends(get_db),
):
    registration = IssuerRegistrationService.get_by_id(db, id_registration)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issuer registration not found",
        )
    return registration

@router.get(
    "/issuer-registrations",
    response_model=IssuerRegistrationListResponse,
)
def get_registrations(
    name: Optional[str] = Query(None),
    status: Optional[IssuerStatus] = Query(None),
    start_date: Optional[int] = Query(None, description="Unix timestamp"),
    end_date: Optional[int] = Query(None, description="Unix timestamp"),
    sort: str = Query("latest", regex="^(latest|oldest)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return IssuerRegistrationService.get_all(
        db=db,
        name=name,
        status=status,
        start_date=start_date,
        end_date=end_date,
        sort=sort,
        page=page,
        page_size=page_size,
    )


@router.patch(
    "/issuer-registrations/{id_registration}/accept",
    response_model=IssuerRegistrationResponse,
)
def accept_registration(
    id_registration: str,
    db: Session = Depends(get_db),
):
    registration = IssuerRegistrationService.accept_registration(
        db, id_registration
    )
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issuer registration not found",
        )
    return registration

@router.patch(
    "/issuer-registrations/{id_registration}/reject",
    response_model=IssuerRegistrationResponse,
)
def reject_registration(
    id_registration: str,
    db: Session = Depends(get_db),
):
    registration = IssuerRegistrationService.reject_registration(
        db, id_registration
    )
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issuer registration not found",
        )
    return registration

@router.delete(
    "/issuer-registrations/{id_registration}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_registration(
    id_registration: str,
    db: Session = Depends(get_db),
):
    success = IssuerRegistrationService.delete_registration(
        db, id_registration
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issuer registration not found",
        )
    return None
