import { ref, computed } from "vue"
import { ethers } from "ethers"

declare global {
  interface Window {
    ethereum?: any
  }
}

export function useWallet() {
  const walletAddress = ref<string | null>(null)
  const provider = ref<ethers.BrowserProvider | null>(null)
  const signer = ref<ethers.Signer | null>(null)
  
  const isConnected = computed(() => !!walletAddress.value)

  const connectWallet = async (): Promise<string> => {
    if (!window.ethereum) {
      throw new Error("MetaMask is not installed. Please install MetaMask to continue.")
    }

    try {
      // Request account access
      const accounts = await window.ethereum.request({ 
        method: "eth_requestAccounts" 
      })
      
      if (!accounts || accounts.length === 0) {
        throw new Error("No accounts found")
      }

      // Setup provider and signer
      provider.value = new ethers.BrowserProvider(window.ethereum)
      signer.value = await provider.value.getSigner()
      walletAddress.value = accounts[0]

      return accounts[0]
    } catch (error: any) {
      if (error.code === 4001) {
        throw new Error("User rejected the connection request")
      }
      throw new Error("Failed to connect wallet: " + error.message)
    }
  }

  const disconnectWallet = () => {
    walletAddress.value = null
    provider.value = null
    signer.value = null
  }

  const signMessage = async (message: string): Promise<string> => {
    if (!signer.value) {
      throw new Error("Wallet not connected")
    }

    try {
      const signature = await signer.value.signMessage(message)
      return signature
    } catch (error: any) {
      if (error.code === 4001) {
        throw new Error("User rejected the signature request")
      }
      throw new Error("Failed to sign message: " + error.message)
    }
  }

  return {
    walletAddress,
    isConnected,
    connectWallet,
    disconnectWallet,
    signMessage
  }
}