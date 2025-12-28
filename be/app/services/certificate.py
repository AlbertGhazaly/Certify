from typing import Optional
from app.models.certificate_key import CertificateKey
from sqlalchemy.orm import Session
import secrets
from app.models.certificate import Certificate
from app.services.read_contract import ContractService
from app.services.ipfs import IPFSService
class CertificateService:
    """Service for managing certificate data"""
    def __init__(self):
        self.contract_service = ContractService()
        self.ipfs_service = IPFSService()
    @staticmethod
    def generate_aes_key() -> str:
        """Generate a random AES-256 key (32 bytes = 256 bits)"""
        return secrets.token_hex(32)  # Returns 64 hex characters = 32 bytes
    
    @staticmethod
    def create_certificate(db: Session, nim: str, aes_key: Optional[str] = None) -> CertificateKey:
        """
        Create a new certificate record
        If aes_key is not provided, a random one will be generated
        """
        if aes_key is None:
            aes_key = CertificateService.generate_aes_key()
        
        certificate = CertificateKey(
            student_id=nim,
            aes_key=aes_key
        )
        
        db.add(certificate)
        db.commit()
        db.refresh(certificate)
        
        return certificate
    
    @staticmethod
    def get_certificate_by_nim(db: Session, nim: str) -> Optional[Certificate]:
        """Get certificate by NIM"""
        return db.query(CertificateKey).filter(CertificateKey.student_id == nim).first()
    
    @staticmethod
    def update_aes_key(db: Session, nim: str, new_aes_key: str) -> Optional[CertificateKey]:
        """Update AES key for a certificate"""
        certificate = db.query(CertificateKey).filter(CertificateKey.student_id == nim).first()
        if certificate:
            certificate.aes_key = new_aes_key
            db.commit()
            db.refresh(certificate)
        return certificate
    
    @staticmethod
    def delete_certificate(db: Session, nim: str) -> bool:
        """Delete certificate by NIM"""
        certificate = db.query(CertificateKey).filter(CertificateKey.student_id == nim).first()
        if certificate:
            db.delete(certificate)
            db.commit()
            return True
        return False
    
    # def verify_certificate(self, db: Session, nim: str) -> bool:
    #     cert = self.contract_service.get_certificate(nim)
    #     if not cert.isValid:
    #         return "Ijazah tidak valid / dicabut"
        
    #     # Download encrypted file from IPFS
    #     encrypted_file = self.ipfs_service.get_file(cert.ipfsCID)
    #     if not encrypted_file:
    #         return "Gagal mengunduh file dari IPFS"
        
    #     # get aes key from database
    #     certificate_key = self.get_certificate_by_nim(db, nim)
    #     if not certificate_key:
    #         return "AES Key tidak ditemukan di database"
    #     aes_key = certificate_key.aes_key

    #     # Decrypt the file using AES key
    #     decrypted_file = AES.decrypt(encrypted_file, aes_key)
    #     hash_calculated = hashlib.sha256(decrypted_file).hexdigest()
    #     if hash_calculated != cert.hash:
    #         return "Hash tidak sesuai, data mungkin telah diubah"
    #     return {
    #         "nim": nim,
    #         "status": "valid",
    #         "file_url": f"https://gateway.pinata.cloud/ipfs/{cert.ipfsCID}"
    #     }