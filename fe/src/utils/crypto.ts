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
