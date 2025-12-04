import { ref } from "vue"
import type { Certificate, Transaction, IssueCertificatePayload } from "@/types"
import { CryptoUtils } from "@/utils/crypto"

export function useBlockchain() {
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const issueCertificate = async (
    payload: IssueCertificatePayload,
    issuerAddress: string,
    signature: string,
  ): Promise<Certificate> => {
    isLoading.value = true
    error.value = null

    try {
      const certificate: Certificate = {
        id: `CERT_${Date.now()}`,
        studentName: payload.studentName,
        studentId: payload.studentId,
        institution: "Institut Teknologi Bandung",
        degree: payload.degree,
        issueDate: new Date().toISOString(),
        signatureHash: signature,
        documentHash: payload.documentHash,
        ipfsCid: payload.ipfsCid,
        issuerAddress,
        status: "active",
        createdAt: new Date().toISOString(),
      }

      // Simulated blockchain transaction
      await new Promise((resolve) => setTimeout(resolve, 1000))

      return certificate
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Failed to issue certificate"
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  const revokeCertificate = async (
    certificateId: string,
    reason: string,
    issuerAddress: string,
    signature: string,
  ): Promise<Transaction> => {
    isLoading.value = true
    error.value = null

    try {
      const transaction: Transaction = {
        id: `TX_${Date.now()}`,
        hash: await CryptoUtils.sha256(`revoke_${certificateId}_${Date.now()}`),
        previousHash: await CryptoUtils.sha256(`genesis_block`),
        type: "revoke",
        certificateId,
        issuerAddress,
        data: { reason },
        signature,
        timestamp: new Date().toISOString(),
        blockNumber: 1,
      }

      // Simulated blockchain transaction
      await new Promise((resolve) => setTimeout(resolve, 1000))

      return transaction
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Failed to revoke certificate"
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  const verifyCertificate = async (certificateId: string, signatureHash: string): Promise<boolean> => {
    isLoading.value = true
    error.value = null

    try {
      // Simulated verification logic
      await new Promise((resolve) => setTimeout(resolve, 500))
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Verification failed"
      return false
    } finally {
      isLoading.value = false
    }
  }

  return {
    isLoading,
    error,
    issueCertificate,
    revokeCertificate,
    verifyCertificate,
  }
}
