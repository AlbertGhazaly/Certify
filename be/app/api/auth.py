from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import ChallengeRequest, ChallengeResponse, VerifyRequest, VerifyResponse, LogoutRequest
from app.database.connection import get_db
from app.services.crypto import AuthCryptoService
from app.services.nonce import NonceService
from app.services.session import SessionService

router = APIRouter(tags=["authentication"])

crypto_service = AuthCryptoService()

@router.post("/challenge", response_model=ChallengeResponse)
def request_challenge(request: ChallengeRequest, db: Session = Depends(get_db)):
    """
    Step 1: Generate authentication challenge
    Client provides wallet address, server generates nonce
    """
    try:
        # Generate nonce
        nonce = crypto_service.generate_nonce()
        
        # Store nonce in database (expires in 5 minutes)
        NonceService.create_nonce(db, request.wallet_address, nonce)
        
        # Create challenge message
        challenge = crypto_service.create_challenge_message(nonce, request.wallet_address)
        
        return ChallengeResponse(challenge=challenge, nonce=nonce)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate challenge: {str(e)}")

@router.post("/verify", response_model=VerifyResponse)
def verify_signature(request: VerifyRequest, db: Session = Depends(get_db)):
    """
    Step 2: Verify signature and authenticate user
    Client signs challenge with private key, server verifies and creates session
    """
    try:
        # Get stored nonce
        nonce_record = NonceService.get_nonce(db, request.wallet_address)
        if not nonce_record:
            raise HTTPException(status_code=400, detail="Challenge expired or not found")
        
        # Recreate challenge message
        challenge = crypto_service.create_challenge_message(nonce_record.nonce, request.wallet_address)
        
        # Verify signature and recover public key
        is_valid, public_key_x, public_key_y = crypto_service.verify_wallet_ownership(
            challenge, 
            request.signature, 
            request.wallet_address
        )
        
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid signature or wallet address mismatch")
        
        # Delete used nonce
        NonceService.delete_nonce(db, request.wallet_address)
        
        # Create session
        session = SessionService.create_session(db, request.wallet_address, public_key_x, public_key_y)
        
        return VerifyResponse(
            success=True,
            message="Authentication successful",
            session_token=request.wallet_address  # In production, use JWT or similar
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
    Check if user has active session
    """
    session = SessionService.get_session(db, wallet_address)
    if session:
        return {
            "active": True,
            "wallet_address": session.wallet_address,
            "created_at": session.created_at
        }
    return {"active": False}