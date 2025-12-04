from eth_account.messages import encode_defunct
from eth_utils import to_checksum_address
from web3 import Web3
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import secrets

class AuthCryptoService:
    def __init__(self):
        self.web3 = Web3()
    
    def generate_nonce(self) -> str:
        """Generate a cryptographically secure random nonce"""
        return secrets.token_hex(32)
    
    def create_challenge_message(self, nonce: str, wallet_address: str) -> str:
        """Create authentication challenge message"""
        return f"Authenticate to Diploma Chain\nWallet: {wallet_address}\nNonce: {nonce}"
    
    def recover_public_key_from_signature(self, message: str, signature: str) -> tuple[str, str]:
        """
        Recover public key from ECDSA signature
        Returns: (public_key_x, public_key_y) as hex strings
        """
        # Encode message for Ethereum signed message
        message_hash = encode_defunct(text=message)
        
        # Recover the address from signature
        recovered_address = self.web3.eth.account.recover_message(message_hash, signature=signature)
        
        # For full public key recovery, we need to use lower-level operations
        # This is a simplified version - in production, use proper key recovery
        from eth_keys import keys
        from eth_utils import decode_hex
        
        # Get the message hash
        msg_hash = message_hash.body
        
        # Recover public key
        signature_bytes = decode_hex(signature)
        v = signature_bytes[-1]
        r = int.from_bytes(signature_bytes[:32], 'big')
        s = int.from_bytes(signature_bytes[32:64], 'big')
        
        # Adjust v for Ethereum's encoding
        if v >= 27:
            v -= 27
        
        from eth_keys.backends import NativeECCBackend
        backend = NativeECCBackend()
        public_key = backend.ecdsa_recover(msg_hash, keys.Signature(vrs=(v, r, s)))
        
        # Extract x and y coordinates
        public_key_bytes = public_key.to_bytes()
        # Remove the 0x04 prefix for uncompressed key
        x = public_key_bytes[1:33].hex()
        y = public_key_bytes[33:65].hex()
        
        return (x, y)
    
    def derive_address_from_public_key(self, public_key_x: str, public_key_y: str) -> str:
        """
        Derive Ethereum address from public key coordinates
        """
        from eth_keys import keys
        from eth_utils import keccak
        
        # Reconstruct public key (uncompressed format: 0x04 + x + y)
        public_key_bytes = bytes.fromhex('04' + public_key_x + public_key_y)
        
        # Hash the public key and take last 20 bytes
        address_bytes = keccak(public_key_bytes[1:])[-20:]
        address = to_checksum_address(address_bytes)
        
        return address
    
    def verify_wallet_ownership(self, message: str, signature: str, wallet_address: str) -> tuple[bool, str, str]:
        """
        Verify wallet ownership by recovering public key and comparing addresses
        Returns: (is_valid, public_key_x, public_key_y)
        """
        try:
            # Recover public key from signature
            public_key_x, public_key_y = self.recover_public_key_from_signature(message, signature)
            
            # Derive address from public key
            derived_address = self.derive_address_from_public_key(public_key_x, public_key_y)
            
            # Compare addresses (case-insensitive)
            is_valid = derived_address.lower() == wallet_address.lower()
            
            return (is_valid, public_key_x, public_key_y)
        except Exception as e:
            print(f"Verification error: {e}")
            return (False, "", "")