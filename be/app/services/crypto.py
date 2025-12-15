from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3
import secrets

class AuthCryptoService:
    def __init__(self):
        self.web3 = Web3()
    
    def generate_nonce(self) -> str:
        """Generate a cryptographically secure random nonce"""
        return secrets.token_hex(32)
    
    def create_challenge_message(self, nonce: str, wallet_address: str) -> str:
        """Create authentication challenge message"""
        return f"Authenticate to Certify\nWallet: {wallet_address}\nNonce: {nonce}"
    
    def verify_wallet_ownership(self, message: str, signature: str, wallet_address: str) -> tuple[bool, str, str]:
        """
        Verify wallet ownership by recovering address from signature
        Returns: (is_valid, public_key_x, public_key_y)
        """
        try:
            # Encode message for Ethereum signed message
            message_hash = encode_defunct(text=message)
            
            # Recover the address from the signature using eth_account
            recovered_address = Account.recover_message(message_hash, signature=signature)
            
            print(f"Recovered address: {recovered_address}")
            print(f"Expected address: {wallet_address}")
            
            # Compare addresses (case-insensitive)
            is_valid = recovered_address.lower() == wallet_address.lower()
            print(is_valid)
            if is_valid:
                # If valid, extract public key from signature
                # Parse signature to get v, r, s
                if signature.startswith('0x'):
                    signature = signature[2:]
                
                signature_bytes = bytes.fromhex(signature)
                r = int.from_bytes(signature_bytes[:32], 'big')
                s = int.from_bytes(signature_bytes[32:64], 'big')
                v = signature_bytes[64]
                
                # Recover public key using eth_keys
                from eth_keys import keys
                from eth_keys.backends import NativeECCBackend
                
                # Adjust v for Ethereum's encoding
                if v >= 27:
                    v -= 27
                
                backend = NativeECCBackend()
                public_key = backend.ecdsa_recover(message_hash.body, keys.Signature(vrs=(v, r, s)))
                
                # Extract x and y coordinates
                public_key_bytes = public_key.to_bytes()
                public_key_x = public_key_bytes[1:33].hex()
                public_key_y = public_key_bytes[33:65].hex()
                
                return (True, public_key_x, public_key_y)
            else:
                return (False, "", "")
                
        except Exception as e:
            print(f"Verification error: {e}")
            import traceback
            traceback.print_exc()
            return (False, "", "")