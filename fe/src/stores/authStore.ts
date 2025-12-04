import { defineStore } from "pinia"
import { ref, computed } from "vue"
import type { User, WalletAuthChallenge } from "@/types"
import { NONCE_EXPIRY_TIME, SESSION_TIMEOUT } from "@/utils/constants"
import { CryptoUtils } from "@/utils/crypto"

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null)
  const authChallenge = ref<WalletAuthChallenge | null>(null)
  const sessionTimer = ref<NodeJS.Timeout | null>(null)

  const isAuthenticated = computed(() => user.value?.isAuthenticated ?? false)
  const userRole = computed(() => user.value?.role)
  const userAddress = computed(() => user.value?.address)

  const generateChallenge = async (): Promise<string> => {
    const nonce = CryptoUtils.generateNonce()
    authChallenge.value = {
      nonce,
      expiresAt: Date.now() + NONCE_EXPIRY_TIME,
    }
    return nonce
  }

  const login = async (address: string, signature: string, role: "admin" | "verifier" | "student") => {
    if (!authChallenge.value || Date.now() > authChallenge.value.expiresAt) {
      throw new Error("Challenge expired. Request a new one.")
    }

    user.value = {
      address,
      role,
      isAuthenticated: true,
    }

    startSessionTimer()
    authChallenge.value = null
  }

  const logout = () => {
    user.value = null
    if (sessionTimer.value) clearTimeout(sessionTimer.value)
  }

  const startSessionTimer = () => {
    if (sessionTimer.value) clearTimeout(sessionTimer.value)
    sessionTimer.value = setTimeout(logout, SESSION_TIMEOUT)
  }

  const setRole = (role: "admin" | "verifier" | "student") => {
    if (user.value) {
      user.value.role = role
    }
  }

  const hasRole = (roles: string | string[]): boolean => {
    if (!user.value) return false
    const roleArray = Array.isArray(roles) ? roles : [roles]
    return roleArray.includes(user.value.role)
  }

  return {
    user,
    isAuthenticated,
    userRole,
    userAddress,
    generateChallenge,
    login,
    logout,
    setRole,
    hasRole,
  }
})
