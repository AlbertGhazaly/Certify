from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class AESEncryptionService:
    @staticmethod
    def generate_key() -> str:
        """Generate a random 256-bit AES key"""
        key = get_random_bytes(32)  # 256 bits
        return base64.b64encode(key).decode('utf-8')
    
    @staticmethod
    def encrypt(data: bytes, key_b64: str) -> bytes:
        """
        Encrypt data using AES-256-CBC
        Returns: IV + encrypted data
        """
        try:
            key = base64.b64decode(key_b64)
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_data = pad(data, AES.block_size)
            encrypted = cipher.encrypt(padded_data)
            return iv + encrypted
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")
    
    @staticmethod
    def decrypt(encrypted_data: bytes, key_b64: str) -> bytes:
        """
        Decrypt data using AES-256-CBC
        Expects: IV + encrypted data
        """
        try:
            key = base64.b64decode(key_b64)
            iv = encrypted_data[:16]
            encrypted = encrypted_data[16:]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(encrypted)
            return unpad(decrypted, AES.block_size)
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")