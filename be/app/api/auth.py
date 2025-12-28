from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import ChallengeRequest, ChallengeResponse, VerifyRequest, VerifyResponse, LogoutRequest
from app.database.connection import get_db
from app.services.crypto import AuthCryptoService
from app.services.nonce import NonceService
from app.services.session import SessionService
from app.services.read_contract import ContractService

router = APIRouter(tags=["authentication"])

crypto_service = AuthCryptoService()
contract_service = ContractService()

@router.post("/challenge", response_model=ChallengeResponse)
def request_challenge(request: ChallengeRequest, db: Session = Depends(get_db)):
    """
    Step 1: Generate authentication challenge
    Client provides wallet address, server generates nonce
    """
    try:
        nonce = crypto_service.generate_nonce()
        
        NonceService.create_nonce(db, request.wallet_address, nonce)
        
        challenge = crypto_service.create_challenge_message(nonce, request.wallet_address)
        
        return ChallengeResponse(challenge=challenge, nonce=nonce)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate challenge: {str(e)}")

@router.post("/verify", response_model=VerifyResponse)
def verify_signature(request: VerifyRequest, db: Session = Depends(get_db)):
    """
    Step 2: Verify signature and authenticate user
    Client signs challenge with private key, server verifies and creates session
    Only issuers can authenticate - validated against Sepolia contract
    """
    try:
        
        nonce_record = NonceService.get_nonce(db, request.wallet_address)
        if not nonce_record:
            raise HTTPException(status_code=400, detail="Challenge expired or not found")
        
        challenge = crypto_service.create_challenge_message(nonce_record.nonce, request.wallet_address)

        is_valid, public_key_x, public_key_y = crypto_service.verify_wallet_ownership(
            challenge, 
            request.signature, 
            request.wallet_address
        )
    
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid signature or wallet address mismatch")
        is_issuer = contract_service.is_issuer(request.wallet_address)
        if not is_issuer:
            NonceService.delete_nonce(db, request.wallet_address)
            raise HTTPException(
                status_code=403, 
                detail="Access denied. Only issuers can authenticate."
            )
        
        NonceService.delete_nonce(db, request.wallet_address)
        
        role = "issuer"
        jwt_token = SessionService.create_jwt_token(request.wallet_address, role)
        
        session = SessionService.create_session(
            db, 
            request.wallet_address, 
            public_key_x, 
            public_key_y,
            role,
            jwt_token
        )
        
        return VerifyResponse(
            success=True,
            message="Authentication successful",
            session_token=request.wallet_address,
            jwt_token=jwt_token,
            role=role,
            wallet_address=request.wallet_address
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@router.post("/logout")
def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    """
    Logout user and remove session
    """
    try:
        success = SessionService.delete_session(db, request.wallet_address)
        if success:
            return {"message": "Logout successful"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")

@router.get("/session/{wallet_address}")
def get_session(wallet_address: str, db: Session = Depends(get_db)):
    """
    Check if user has active session and validate issuer status
    """
    session = SessionService.get_session(db, wallet_address)
    if session:
        payload = SessionService.verify_jwt_token(session.jwt_token)
        if payload:
            is_issuer = contract_service.is_issuer(wallet_address)
            if is_issuer:
                return {
                    "active": True,
                    "wallet_address": session.wallet_address,
                    "role": session.role,
                    "created_at": session.created_at
                }
    
    return {"active": False}

@router.get("/validate-token")
def validate_token(token: str, db: Session = Depends(get_db)):
    """
    Validate JWT token and return session info
    """
    session = SessionService.validate_session_token(db, token)
    if session:
        is_issuer = contract_service.is_issuer(session.wallet_address)
        if is_issuer:
            return {
                "valid": True,
                "wallet_address": session.wallet_address,
                "role": session.role
            }
    
    return {"valid": False}