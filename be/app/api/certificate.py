from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.certificate import (
    IssueCertificateRequest, 
    IssueCertificateResponse,
    PublicVerifyRequest,
    PublicVerifyResponse, 
    VerifyCertificateRequest, 
    VerifyCertificateResponse,
    SignCertificateRequest,
    SignCertificateResponse
)
from app.database.connection import get_db
from app.services.ipfs import IPFSService
from app.services.encryption import AESEncryptionService
from app.services.read_contract import ContractService
from app.services.certificate import CertificateService
from app.models.certificate_key import CertificateKey
import hashlib
from datetime import datetime
from urllib.parse import quote

router = APIRouter(tags=["certificate"])

ipfs_service = IPFSService()
encryption_service = AESEncryptionService()
contract_service = ContractService()
certificate_service = CertificateService()

# Template ijazah Indonesia
IJAZAH_TEMPLATE = """Kementerian Pendidikan Tinggi, Sains, dan Teknologi
Institut Teknologi Bandung

dengan ini menyatakan bahwa

{student_name}
NIM {student_id}

lahir di {birth_place}, tanggal {birth_date}, telah menyelesaikan dengan baik dan sudah memenuhi semua persyaratan pada Program Studi {degree}

Oleh sebab itu kepadanya diberikan gelar

SARJANA TEKNIK

beserta hak dan segala kewajiban yang melekat pada gelar tersebut. Diberikan di Bandung tanggal {issue_date}

Rektor

     

Prof. Dr. Ir. Tatacipta Dirgantara, M.T.
NIP: 1243568790
"""

@router.post("/issue", response_model=IssueCertificateResponse)
async def issue_certificate(
    request: IssueCertificateRequest,
    db: Session = Depends(get_db)
):
    """
    Issue a new certificate
    Flow: Generate txt -> Encrypt -> Upload to IPFS -> Store key -> Return for signing
    """
    try:
        if contract_service.certificate_exists(request.student_id):
            raise HTTPException(status_code=400, detail="Certificate already exists for this student ID")
        
        certificate_text = IJAZAH_TEMPLATE.format(
            student_name=request.student_name,
            student_id=request.student_id,
            birth_place=request.birth_place,
            birth_date=request.birth_date,
            degree=request.degree,
            issue_date=request.issue_date
        )
        
        aes_key = encryption_service.generate_key()
        
        certificate_bytes = certificate_text.encode('utf-8')
        encrypted_data = encryption_service.encrypt(certificate_bytes, aes_key)
        
        ipfs_cid = ipfs_service.upload_file(
            encrypted_data,
            f"certificate_{request.student_id}.enc"
        )
        
        if not ipfs_cid:
            raise HTTPException(status_code=500, detail="Failed to upload to IPFS")
        
        cert_hash = hashlib.sha256(certificate_bytes).hexdigest()
        
        cert_key = CertificateKey(
            student_id=request.student_id,
            aes_key=aes_key
        )
        db.add(cert_key)
        db.commit()
        
        return IssueCertificateResponse(
            success=True,
            message="Certificate prepared. Please sign and submit to blockchain.",
            student_id=request.student_id,
            ipfs_cid=ipfs_cid,
            cert_hash=cert_hash,
            aes_key=aes_key
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to issue certificate: {str(e)}")

@router.post("/verify", response_model=VerifyCertificateResponse)
async def verify_certificate(
    request: VerifyCertificateRequest,
    db: Session = Depends(get_db)
):
    try:
        if not contract_service.certificate_exists(request.student_id):
            return VerifyCertificateResponse(
                success=False,
                valid=False,
                message="Certificate not found on blockchain"
            )

        is_valid = contract_service.is_certificate_valid(request.student_id)

        cert_data = contract_service.get_certificate(request.student_id)
        if not cert_data:
            return VerifyCertificateResponse(
                success=False,
                valid=False,
                message="Failed to retrieve certificate data"
            )

        ipfs_cid = cert_data["ipfsCID"]
        file_url = ipfs_service.get_gateway_url(ipfs_cid)

        encrypted_data = ipfs_service.get_file(ipfs_cid)
        if not encrypted_data:
            return VerifyCertificateResponse(
                success=False,
                valid=is_valid,
                message="Failed to retrieve certificate from IPFS",
                ipfs_cid=ipfs_cid,
                file_url=file_url
            )

        certificate_key = certificate_service.get_certificate_by_nim(db, request.student_id)
        if not certificate_key:
            raise HTTPException(status_code=404, detail="AES key not found")

        aes_key = certificate_key.aes_key

        try:
            decrypted_data = encryption_service.decrypt(encrypted_data, aes_key)
            certificate_text = decrypted_data.decode("utf-8")
        except Exception:
            return VerifyCertificateResponse(
                success=False,
                valid=is_valid,
                message="Invalid decryption key",
                ipfs_cid=ipfs_cid,
                file_url=file_url
            )

        calculated_hash = hashlib.sha256(decrypted_data).hexdigest()
        blockchain_hash = cert_data["certHash"]

        if calculated_hash != blockchain_hash:
            return VerifyCertificateResponse(
                success=False,
                valid=False,
                message="Certificate hash mismatch",
                ipfs_cid=ipfs_cid,
                file_url=file_url
            )
        
        verify_url = (
            "http://localhost:3000/verify"
            f"?cid={quote(ipfs_cid)}"
            f"&key={quote(aes_key)}"
            f"&hash={quote(blockchain_hash)}"
        )

        certificate_text_with_url = (
            certificate_text
            + "\n\nVerifikasi Keaslian Ijazah:\n"
            + verify_url
        )


        return VerifyCertificateResponse(
            success=True,
            valid=is_valid,
            certificate_text=certificate_text_with_url,
            ipfs_cid=ipfs_cid,
            file_url=verify_url,
            message="Certificate verified successfully"
            if is_valid else "Certificate has been revoked"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@router.post("/verify-public", response_model=PublicVerifyResponse)
async def verify_certificate_public(request: PublicVerifyRequest):
    try:
        file_url = ipfs_service.get_gateway_url(request.ipfs_cid)

        # 1. Download encrypted data
        encrypted_data = ipfs_service.get_file(request.ipfs_cid)
        if not encrypted_data:
            return PublicVerifyResponse(
                success=False,
                valid=False,
                message="Failed to retrieve certificate from IPFS",
                file_url=file_url
            )

        # 2. Decrypt
        try:
            decrypted_data = encryption_service.decrypt(
                encrypted_data,
                request.aes_key
            )
            certificate_text = decrypted_data.decode("utf-8")
        except Exception:
            return PublicVerifyResponse(
                success=False,
                valid=False,
                message="Invalid AES key",
                file_url=file_url
            )

        # 3. Verify hash
        calculated_hash = hashlib.sha256(decrypted_data).hexdigest()
        if calculated_hash != request.cert_hash:
            return PublicVerifyResponse(
                success=False,
                valid=False,
                message="Certificate hash mismatch",
                file_url=file_url
            )

        # # 4. Verify on blockchain
        # if not contract_service.is_hash_issued(request.cert_hash):
        #     return PublicVerifyResponse(
        #         success=False,
        #         valid=False,
        #         message="Certificate not registered on blockchain",
        #         file_url=file_url
        #     )
        verify_url = (
            "http://localhost:3000/verify"
            f"?cid={quote(request.ipfs_cid)}"
            f"&key={quote(request.aes_key)}"
            f"&hash={quote(request.cert_hash)}"
        )
        certificate_text_with_url = (
            certificate_text
            + "\n\nVerifikasi Keaslian Ijazah:\n"
            + verify_url
        )
        return PublicVerifyResponse(
            success=True,
            valid=True,
            message="Certificate verified successfully",
            certificate_text=certificate_text_with_url,
            file_url=verify_url
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/key/{student_id}")
async def get_certificate_key(student_id: str, db: Session = Depends(get_db)):
    """
    Get AES key for a certificate (admin only in production)
    """
    cert_key = db.query(CertificateKey).filter(CertificateKey.student_id == student_id).first()
    if not cert_key:
        raise HTTPException(status_code=404, detail="Key not found")
    
    return {"student_id": student_id, "aes_key": cert_key.aes_key}

@router.get("/blockchain/all")
async def get_all_certificates_from_blockchain():
    """Get all certificates from blockchain smart contract"""
    try:
        certificates = contract_service.get_all_certificates()
        return {
            "success": True,
            "certificates": certificates,
            "count": len(certificates)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch certificates from blockchain: {str(e)}"
        )

@router.post("/sign/prepare", response_model=SignCertificateResponse)
async def prepare_certificate_signing(
    request: SignCertificateRequest,
    db: Session = Depends(get_db)
):
    """
    Prepare certificate data for signing
    Returns certificate hash and blockchain data for frontend to sign
    """
    try:
        if not contract_service.certificate_exists(request.student_id):
            raise HTTPException(status_code=404, detail="Certificate not found on blockchain")
        
        cert_data = contract_service.get_certificate(request.student_id)
        if not cert_data:
            raise HTTPException(status_code=404, detail="Failed to retrieve certificate data")
        
        return SignCertificateResponse(
            success=True,
            message="Certificate data retrieved. Ready for signing.",
            student_id=request.student_id,
            cert_hash=cert_data['certHash'],
            ipfs_cid=cert_data['ipfsCID'],
            certificate_data=cert_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to prepare signing: {str(e)}")
