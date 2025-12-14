from web3 import Web3
from typing import Tuple

class ContractService:
    def __init__(self):
        # Configure your RPC endpoint (e.g., Infura, Alchemy, or local node)
        self.w3 = Web3(Web3.HTTPProvider('YOUR_RPC_ENDPOINT'))
        self.contract_address = '0xC0d836b1BA516aF8FA555bcF55963c5c5A9E8728'
        
        # ABI for the role check functions from DiplomaContract
        self.contract_abi = [
            {
                "inputs": [{"name": "walletId", "type": "address"}],
                "name": "isAdmin",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "walletId", "type": "address"}],
                "name": "isInstitution",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "walletId", "type": "address"}],
                "name": "isStudent",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=self.contract_abi
        )
    
    def get_user_role(self, wallet_address: str) -> str:
        """
        Check wallet address against contract and return role
        Priority: admin (institution or admin) > student > verifier
        Returns: 'admin', 'student', or 'verifier'
        """
        try:
            checksum_address = Web3.to_checksum_address(wallet_address)
            
            # Check institution first (highest priority)
            is_institution = self.contract.functions.isInstitution(checksum_address).call()
            if is_institution:
                return "admin"
            
            # Check admin
            is_admin = self.contract.functions.isAdmin(checksum_address).call()
            if is_admin:
                return "admin"
            
            # Check student
            is_student = self.contract.functions.isStudent(checksum_address).call()
            if is_student:
                return "student"
            
            # Default role if none of the above
            return "verifier"
        except Exception as e:
            # If contract read fails, default to verifier
            print(f"Contract read error: {str(e)}")
            return "verifier"