import { defineStore } from "pinia"
import { ref, computed } from "vue"
import type { User } from "@/types"
import axios from "axios"

const API_URL = "http://localhost:8000/api"
const STORAGE_KEY = "auth"
const TOKEN_KEY = "jwt_token"

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null)
  const walletAddress = ref<string>("")
  const jwtToken = ref<string>("")
  const isReady = ref(false)

  const isAuthenticated = computed(() => user.value?.isAuthenticated ?? false)
  const userRole = computed(() => user.value?.role)
  const userAddress = computed(() => user.value?.address)

  // Setup axios interceptor to include JWT token in all requests
  const setupAxiosInterceptor = () => {
    axios.interceptors.request.use(
      (config) => {
        if (jwtToken.value) {
          config.headers.Authorization = `Bearer ${jwtToken.value}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )
  }

  const init = async () => {
    const saved = localStorage.getItem(STORAGE_KEY)
    const token = localStorage.getItem(TOKEN_KEY)
    
    if (saved && token) {
      user.value = JSON.parse(saved)
      jwtToken.value = token
      setupAxiosInterceptor()
      
      // Validate token with backend
      const isValid = await validateToken(token)
      if (!isValid) {
        // Token invalid, clear session
        await logout()
      }
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
        // Store JWT token
        jwtToken.value = response.data.jwt_token
        localStorage.setItem(TOKEN_KEY, response.data.jwt_token)
        
        // Store user info
        user.value = {
          address: response.data.wallet_address,
          role: response.data.role, // Should be "issuer"
          isAuthenticated: true
        }
        localStorage.setItem(STORAGE_KEY, JSON.stringify(user.value))
        
        // Setup axios interceptor with new token
        setupAxiosInterceptor()
        
        return true
      }
      return false
    } catch (error: any) {
      if (error.response?.status === 403) {
        throw new Error("Access denied. Only issuers can authenticate.")
      }
      throw new Error("Signature verification failed")
    }
  }

  const validateToken = async (token: string): Promise<boolean> => {
    try {
      const response = await axios.get(`${API_URL}/auth/validate-token`, {
        params: { token }
      })
      return response.data.valid
    } catch (error) {
      return false
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
    jwtToken.value = ""
    localStorage.removeItem(STORAGE_KEY)
    localStorage.removeItem(TOKEN_KEY)
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
    jwtToken,
    isAuthenticated,
    userRole,
    userAddress,
    isReady,
    init,
    requestChallenge,
    verifySignature,
    validateToken,
    logout,
    checkSession
  }
})