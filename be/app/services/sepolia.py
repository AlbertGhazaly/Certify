from fastapi import HTTPException
from web3 import Web3

class SepoliaService:
    def __init__(self, infura_url: str):
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        if not self.web3.isConnected():
            raise HTTPException(status_code=500, detail="Unable to connect to Sepolia network")

    def get_balance(self, address: str) -> float:
        balance_wei = self.web3.eth.get_balance(address)
        return self.web3.fromWei(balance_wei, 'ether')

    def send_transaction(self, from_address: str, to_address: str, amount: float, private_key: str) -> str:
        nonce = self.web3.eth.getTransactionCount(from_address)
        transaction = {
            'to': to_address,
            'value': self.web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce,
        }
        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return self.web3.toHex(txn_hash)