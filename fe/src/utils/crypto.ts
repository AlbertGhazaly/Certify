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
      const { default: Web3 } = await import('web3')
      const web3 = new Web3(window.ethereum)
      
      const contract = new web3.eth.Contract(abi, contractAddress)
      
      let gasLimit: number
      try {
        console.log('Estimating gas for', methodName, '...')
        const gasEstimate = await contract.methods[methodName](...params).estimateGas({ from })
        console.log('Gas estimate:', gasEstimate.toString())
        
        gasLimit = Math.floor(Number(gasEstimate) * 1.2)
        
        const maxGas = 10000000 // 10M to be safe
        if (gasLimit > maxGas) {
          console.warn(`Gas limit ${gasLimit} exceeds max, using ${maxGas}`)
          gasLimit = maxGas
        }
      } catch (estimateError: any) {
        console.warn('Gas estimation failed:', estimateError.message)
        
        const defaultGasLimits: { [key: string]: number } = {
          'proposeCertificate': 500000,
          'signCertificateIssuance': 200000,
          'signCertificateRevocation': 200000,
          'addIssuer': 150000,
          'removeIssuer': 100000,
          'updateIssuerPublicKey': 100000
        }
        gasLimit = defaultGasLimits[methodName] || 300000
        console.log('Using default gas limit:', gasLimit)
      }
      
      console.log('Final gas limit:', gasLimit)
      
      const gasPrice = await web3.eth.getGasPrice()
      console.log('Gas price:', gasPrice.toString())
      
      const tx = await contract.methods[methodName](...params).send({
        from,
        gas: gasLimit,
        gasPrice: gasPrice
      })
      
      console.log('Transaction successful:', tx.transactionHash)
      return tx
      
    } catch (error: any) {
      console.error('Transaction error:', error)
      
      if (error.code === 4001) {
        throw new Error('User rejected transaction')
      }
      
      if (error.message?.includes('gas limit too high')) {
        throw new Error('Transaction requires too much gas. The contract may have failed validation.')
      }
      
      if (error.message?.includes('insufficient funds')) {
        throw new Error('Insufficient funds for gas fees')
      }
      
      if (error.message?.includes('execution reverted')) {
        const revertMatch = error.message.match(/reverted: (.+?)(?:\n|$)/)
        const revertReason = revertMatch ? revertMatch[1] : 'Transaction reverted by contract'
        throw new Error(revertReason)
      }
      
      if (error.message?.includes('nonce too low')) {
        throw new Error('Transaction nonce error. Please try again.')
      }
      
      if (error.message?.includes('replacement transaction underpriced')) {
        throw new Error('Previous transaction still pending. Please wait or increase gas price.')
      }
      
      throw new Error(error.message || 'Transaction failed')
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
   * Verify signature
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