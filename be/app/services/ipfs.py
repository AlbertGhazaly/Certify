import requests
import os
from typing import Optional
from io import BytesIO

class IPFSService:
    def __init__(self):
        self.ipfs_url = os.getenv('IPFS_URL', 'http://127.0.0.1:5001')
        self.gateway_url = os.getenv('IPFS_GATEWAY', 'http://127.0.0.1:8080/ipfs')
    
    def upload_file(self, file_content: bytes, filename: str) -> Optional[str]:
        """
        Upload file to IPFS and return CID
        """
        try:
            files = {
                'file': (filename, BytesIO(file_content))
            }
            response = requests.post(
                f'{self.ipfs_url}/api/v0/add',
                files=files,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            cid = result['Hash']
            print(f"File uploaded to IPFS: {cid}")
            return cid
        except Exception as e:
            print(f"Error uploading to IPFS: {str(e)}")
            return None
    
    def get_file(self, cid: str) -> Optional[bytes]:
        """
        Retrieve file from IPFS by CID
        """
        try:
            response = requests.get(
                f'{self.ipfs_url}/api/v0/cat?arg={cid}',
                timeout=30
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Error retrieving from IPFS: {str(e)}")
            return None
    
    def get_gateway_url(self, cid: str) -> str:
        """
        Get public gateway URL for CID
        """
        return f"{self.gateway_url}/{cid}"