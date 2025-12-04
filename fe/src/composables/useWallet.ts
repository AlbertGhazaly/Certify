import { ref, computed } from "vue"
import { CryptoUtils } from "@/utils/crypto"

export function useWallet() {
  const walletAddress = ref<string | null>(null)
  const isConnected = computed(() => !!walletAddress)

  const connectWallet = async (): Promise<string> => {
    // Simulated wallet connection
    // In production, use ethers.js or web3.js
    const mockAddress =
      "0x" +
      Array(40)
        .fill(0)
        .map(() => Math.floor(Math.random() * 16).toString(16))
        .join("")
    walletAddress.value = mockAddress
    return mockAddress
  }

  const disconnectWallet = () => {
    walletAddress.value = null
  }

  const signMessage = async (message: string): Promise<string> => {
    if (!walletAddress.value) throw new Error("Wallet not connected")

    const signature = await CryptoUtils.sign(message, walletAddress.value)
    return signature.signature
  }

  const verifySignature = async (message: string, signature: string): Promise<boolean> => {
    if (!walletAddress.value) return false
    return CryptoUtils.verify(message, signature, walletAddress.value)
  }

  return {
    walletAddress,
    isConnected,
    connectWallet,
    disconnectWallet,
    signMessage,
    verifySignature,
  }
}
