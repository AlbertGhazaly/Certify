from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
import json
import os

def generate_ecc_keys():
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    public_key = private_key.public_key()
    
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw
    )
    
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    
    return private_key_bytes, public_key_bytes

def store_keys_in_local_storage(private_key):
    local_storage_path = os.path.join(os.getcwd(), 'local_storage.json')
    if os.path.exists(local_storage_path):
        with open(local_storage_path, 'r') as file:
            storage = json.load(file)
    else:
        storage = {}
    
    storage['private_key'] = private_key.hex()
    
    with open(local_storage_path, 'w') as file:
        json.dump(storage, file)

def store_keys_in_ipfs(private_key):
    # Placeholder for IPFS storage logic
    pass

def main():
    private_key, public_key = generate_ecc_keys()
    store_keys_in_local_storage(private_key)
    store_keys_in_ipfs(private_key)

if __name__ == "__main__":
    main()