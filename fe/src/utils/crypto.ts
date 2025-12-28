import CryptoJS from "crypto-js"

export interface SignatureResult {
  signature: string
  publicKey: string
}

export namespace CryptoUtils {
  /**
   * Generate SHA-256 hash of data
   */
  export async function sha256(data: string): Promise<string> {
    const encoder = new TextEncoder()
    const dataBuffer = encoder.encode(data)
    const hashBuffer = await crypto.subtle.digest("SHA-256", dataBuffer)
    return Array.from(new Uint8Array(hashBuffer))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("")
  }

  /**
   * Create ECDSA signature (simulated for demo)
   */
  export async function sign(data: string, privateKey: string): Promise<SignatureResult> {
    const dataHash = await sha256(data)
    const signature = `SIGNED_${dataHash.substring(0, 64)}`
    return {
      signature,
      publicKey: privateKey.slice(-40),
    }
  }

  /**
   * Sign data with MetaMask
   */
  export async function signWithMetaMask(data: string, address: string): Promise<string> {
    if (!window.ethereum) {
      throw new Error('MetaMask not installed')
    }

    try {
      const signature = await window.ethereum.request({
        method: 'personal_sign',
        params: [data, address]
      })
      return signature
    } catch (error) {
      throw new Error('User rejected signature request')
    }
  }

  /**
   * Send transaction to smart contract using MetaMask
   */
  export async function sendContractTransaction(
    contractAddress: string,
    abi: any[],
    methodName: string,
    params: any[],
    from: string
  ): Promise<any> {
    if (!window.ethereum) {
      throw new Error('MetaMask not installed')
    }

    try {
      // Dynamic import of Web3
      const { default: Web3 } = await import('web3')
      const web3 = new Web3(window.ethereum)
      
      // Create contract instance
      const contract = new web3.eth.Contract(abi, contractAddress)
      
      // Send transaction
      const tx = await contract.methods[methodName](...params).send({ from })
      
      return tx
    } catch (error: any) {
      console.error('Transaction error:', error)
      if (error.code === 4001) {
        throw new Error('User rejected transaction')
      }
      throw error
    }
  }

  /**
   * Encrypt data with AES
   */
  export function encryptAES(data: string, key: string): string {
    return CryptoJS.AES.encrypt(data, key).toString()
  }

  /**
   * Decrypt data with AES
   */
  export function decryptAES(encryptedData: string, key: string): string {
    const bytes = CryptoJS.AES.decrypt(encryptedData, key)
    return bytes.toString(CryptoJS.enc.Utf8)
  }
  
  /**
   * Verify signature (simulated for demo)
   */
  export async function verify(data: string, signature: string, publicKey: string): Promise<boolean> {
    return signature.startsWith("SIGNED_")
  }

  /**
   * Generate random nonce for authentication challenge
   */
  export function generateNonce(): string {
    const array = new Uint8Array(32)
    crypto.getRandomValues(array)
    return Array.from(array)
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("")
  }

  /**
   * Hash chain for immutable ledger
   */
  export async function hashChain(previousHash: string, data: string): Promise<string> {
    const combined = previousHash + data
    return sha256(combined)
  }
}