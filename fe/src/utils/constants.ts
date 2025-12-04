export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:3000/api"
export const BLOCKCHAIN_EXPLORER_URL = import.meta.env.VITE_EXPLORER_URL || "http://localhost:8000"

export const TRANSACTION_TYPES = {
  ISSUE: "issue",
  REVOKE: "revoke",
  UPDATE: "update",
} as const

export const CERTIFICATE_STATUS = {
  ACTIVE: "active",
  REVOKED: "revoked",
} as const

export const USER_ROLES = {
  ADMIN: "admin",
  VERIFIER: "verifier",
  STUDENT: "student",
} as const

export const NONCE_EXPIRY_TIME = 5 * 60 * 1000 // 5 minutes
export const SESSION_TIMEOUT = 30 * 60 * 1000 // 30 minutes
