import { defineStore } from "pinia"
import { ref, computed } from "vue"
import type { User } from "@/types"
import axios from "axios"

const API_URL = "http://localhost:8000/api"
const STORAGE_KEY = "auth"

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null)
  const walletAddress = ref<string>("")
  const isReady = ref(false)

  const isAuthenticated = computed(() => user.value?.isAuthenticated ?? false)
  const userRole = computed(() => user.value?.role)
  const userAddress = computed(() => user.value?.address)

  const init = () => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      user.value = JSON.parse(saved)
    }
    isReady.value = true
  }

  const requestChallenge = async (address: string): Promise<{ challenge: string; nonce: string }> => {
    try {
      const response = await axios.post(`${API_URL}/auth/challenge`, {
        wallet_address: address
      })
      walletAddress.value = address
      return response.data
    } catch (error) {
      throw new Error("Failed to request challenge")
    }
  }

  const verifySignature = async (address: string, signature: string): Promise<boolean> => {
    try {
      const response = await axios.post(`${API_URL}/auth/verify`, {
        wallet_address: address,
        signature: signature
      })
      
      if (response.data.success) {
        // console.log("response: ", response.data)
        user.value = {
          address: address,
          role: "admin", // Default role, can be fetched from backend
          isAuthenticated: true
        }
        localStorage.setItem(STORAGE_KEY, JSON.stringify(user.value))
        return true
      }
      return false
    } catch (error) {
      throw new Error("Signature verification failed")
    }
  }

  const logout = async () => {
    if (user.value?.address) {
      try {
        await axios.post(`${API_URL}/auth/logout`, {
          wallet_address: user.value.address
        })
      } catch (error) {
        console.error("Logout error:", error)
      }
    }
    user.value = null
    walletAddress.value = ""
    localStorage.removeItem(STORAGE_KEY)
  }

  const checkSession = async (address: string): Promise<boolean> => {
    try {
      const response = await axios.get(`${API_URL}/auth/session/${address}`)
      return response.data.active
    } catch (error) {
      return false
    }
  }

  return {
    user,
    isAuthenticated,
    userRole,
    userAddress,
    init,
    requestChallenge,
    verifySignature,
    logout,
    checkSession
  }
})