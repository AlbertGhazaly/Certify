from web3 import Web3
from typing import Optional, Dict, List, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class ContractService:
    def __init__(self):
        rpc_url = os.getenv('SEPOLIA_URL')
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        
        if not rpc_url:
            raise ValueError("SEPOLIA_URL environment variable is not set")
        if not self.contract_address:
            raise ValueError("CONTRACT_ADDRESS environment variable is not set")
        
        print(f"Loaded SEPOLIA_URL: {rpc_url}")
        print(f"Loaded CONTRACT_ADDRESS: {self.contract_address}")
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        self.contract_abi = [
            # Issuer Management - Read Functions
            {
                "inputs": [{"name": "walletId", "type": "address"}],
                "name": "isIssuer",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getIssuerList",
                "outputs": [{"name": "", "type": "address[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "walletId", "type": "address"}],
                "name": "getIssuer",
                "outputs": [
                    {"name": "walletId", "type": "address"},
                    {"name": "publicKey", "type": "string"},
                    {"name": "isActive", "type": "bool"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            # Certificate Management - Read Functions
            {
                "inputs": [{"name": "studentId", "type": "string"}],
                "name": "getCertificate",
                "outputs": [
                    {"name": "_studentId", "type": "string"},
                    {"name": "certHash", "type": "bytes32"},
                    {"name": "ipfsCID", "type": "string"},
                    {"name": "issuerWallets", "type": "address[]"},
                    {"name": "issueSignatureCount", "type": "uint256"},
                    {"name": "revokeSignatureCount", "type": "uint256"},
                    {"name": "isValid", "type": "bool"},
                    {"name": "timestampIssued", "type": "uint256"},
                    {"name": "timestampLastUpdated", "type": "uint256"},
                    {"name": "revokeReason", "type": "string"},
                    {"name": "requiresAllSignatures", "type": "bool"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "studentId", "type": "string"},
                    {"name": "issuer", "type": "address"}
                ],
                "name": "getIssueSignature",
                "outputs": [{"name": "", "type": "bytes"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "studentId", "type": "string"},
                    {"name": "issuer", "type": "address"}
                ],
                "name": "getRevokeSignature",
                "outputs": [{"name": "", "type": "bytes"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "studentId", "type": "string"}],
                "name": "certificateExistsFor",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "studentId", "type": "string"}],
                "name": "isCertificateValid",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getAllCertificates",
                "outputs": [
                    {"name": "studentIds", "type": "string[]"},
                    {"name": "certHashes", "type": "bytes32[]"},
                    {"name": "ipfsCIDs", "type": "string[]"},
                    {"name": "isValids", "type": "bool[]"},
                    {"name": "timestampsIssued", "type": "uint256[]"},
                    {"name": "timestampsLastUpdated", "type": "uint256[]"},
                    {"name": "revokeReasons", "type": "string[]"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=self.contract_abi
        )
    
    # ========== ISSUER READ FUNCTIONS ==========
    
    def is_issuer(self, wallet_address: str) -> bool:
        """
        Check if an address is an active issuer
        """
        try:
            checksum_address = Web3.to_checksum_address(wallet_address)
            return self.contract.functions.isIssuer(checksum_address).call()
        except Exception as e:
            print(f"Error checking issuer status: {str(e)}")
            return False
    
    def get_user_role(self, wallet_address: str) -> str:
        """
        Check wallet address against contract and return role
        Returns: 'admin' or 'verifier'
        """
        try:
            if self.is_issuer(wallet_address):
                return "admin"
            return "verifier"
        except Exception as e:
            print(f"Contract read error: {str(e)}")
            return "verifier"
    
    def get_issuer_list(self) -> List[str]:
        """
        Get list of all issuer addresses
        """
        try:
            issuers = self.contract.functions.getIssuerList().call()
            return [str(issuer) for issuer in issuers]
        except Exception as e:
            print(f"Error getting issuer list: {str(e)}")
            return []
    
    def get_issuer(self, wallet_address: str) -> Optional[Dict]:
        """
        Get issuer details
        Returns: {walletId, publicKey, isActive}
        """
        try:
            checksum_address = Web3.to_checksum_address(wallet_address)
            issuer = self.contract.functions.getIssuer(checksum_address).call()
            return {
                "walletId": issuer[0],
                "publicKey": issuer[1],
                "isActive": issuer[2]
            }
        except Exception as e:
            print(f"Error getting issuer: {str(e)}")
            return None
    
    # ========== CERTIFICATE READ FUNCTIONS ==========
    
    def certificate_exists(self, student_id: str) -> bool:
        """
        Check if a certificate exists for a student ID
        """
        try:
            return self.contract.functions.certificateExistsFor(student_id).call()
        except Exception as e:
            print(f"Error checking certificate existence: {str(e)}")
            return False
    
    def is_certificate_valid(self, student_id: str) -> bool:
        """
        Check if a certificate is valid (not revoked)
        """
        try:
            return self.contract.functions.isCertificateValid(student_id).call()
        except Exception as e:
            print(f"Error checking certificate validity: {str(e)}")
            return False
    
    def get_certificate(self, student_id: str) -> Optional[Dict]:
        """
        Get full certificate details
        Returns: Certificate data dictionary or None if not found
        """
        try:
            cert = self.contract.functions.getCertificate(student_id).call()
            return {
                "studentId": cert[0],
                "certHash": cert[1].hex(),
                "ipfsCID": cert[2],
                "issuerWallets": [str(addr) for addr in cert[3]],
                "issueSignatureCount": cert[4],
                "revokeSignatureCount": cert[5],
                "isValid": cert[6],
                "timestampIssued": cert[7],
                "timestampLastUpdated": cert[8],
                "revokeReason": cert[9],
                "requiresAllSignatures": cert[10]
            }
        except Exception as e:
            print(f"Error getting certificate: {str(e)}")
            return None
    
    def get_issue_signature(self, student_id: str, issuer_address: str) -> Optional[str]:
        """
        Get the issue signature from a specific issuer for a certificate
        """
        try:
            checksum_address = Web3.to_checksum_address(issuer_address)
            signature = self.contract.functions.getIssueSignature(student_id, checksum_address).call()
            return signature.hex() if signature else None
        except Exception as e:
            print(f"Error getting issue signature: {str(e)}")
            return None
    
    def get_revoke_signature(self, student_id: str, issuer_address: str) -> Optional[str]:
        """
        Get the revoke signature from a specific issuer for a certificate
        """
        try:
            checksum_address = Web3.to_checksum_address(issuer_address)
            signature = self.contract.functions.getRevokeSignature(student_id, checksum_address).call()
            return signature.hex() if signature else None
        except Exception as e:
            print(f"Error getting revoke signature: {str(e)}")
            return None
    
    def get_all_certificate_signatures(self, student_id: str) -> Dict[str, List[Dict]]:
        """
        Get all signatures (issue and revoke) for a certificate
        """
        try:
            cert = self.get_certificate(student_id)
            if not cert:
                return {"issueSignatures": [], "revokeSignatures": []}
            
            issue_sigs = []
            revoke_sigs = []
            
            for issuer in cert["issuerWallets"]:
                issue_sig = self.get_issue_signature(student_id, issuer)
                if issue_sig:
                    issue_sigs.append({"issuer": issuer, "signature": issue_sig})
                
                revoke_sig = self.get_revoke_signature(student_id, issuer)
                if revoke_sig:
                    revoke_sigs.append({"issuer": issuer, "signature": revoke_sig})
            
            return {
                "issueSignatures": issue_sigs,
                "revokeSignatures": revoke_sigs
            }
        except Exception as e:
            print(f"Error getting all signatures: {str(e)}")
            return {"issueSignatures": [], "revokeSignatures": []}
    
    def get_all_certificates(self) -> List[Dict]:
        """
        Get all certificates from the smart contract
        Returns: List of certificate dictionaries
        """
        try:
            result = self.contract.functions.getAllCertificates().call()
            
            certificates = []
            for i in range(len(result[0])):
                certificates.append({
                    "studentId": result[0][i],
                    "certHash": result[1][i].hex(),
                    "ipfsCID": result[2][i],
                    "isValid": result[3][i],
                    "timestampIssued": result[4][i],
                    "timestampLastUpdated": result[5][i],
                    "revokeReason": result[6][i]
                })
            
            return certificates
        except Exception as e:
            print(f"Error getting all certificates: {str(e)}")
            return []