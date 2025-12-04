// Cryptography-related types

export interface KeyPair {
  publicKey: string
  privateKey: string
}

export interface SignatureResult {
  signature: string
  publicKey: string
}

export interface EncryptionResult {
  ciphertext: string
  iv: string
  salt: string
}

export interface DecryptionResult {
  plaintext: string
}

export interface HashResult {
  hash: string
  algorithm: "SHA-256" | "SHA-384" | "SHA-512"
}
