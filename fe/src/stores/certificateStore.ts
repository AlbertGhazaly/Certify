import { defineStore } from "pinia"
import { ref, computed } from "vue"
import type { Certificate, Transaction } from "@/types"

export const useCertificateStore = defineStore("certificate", () => {
  const certificates = ref<Certificate[]>([])
  const transactions = ref<Transaction[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const activeCertificates = computed(() => certificates.value.filter((c) => c.status === "active"))

  const revokedCertificates = computed(() => certificates.value.filter((c) => c.status === "revoked"))

  const getCertificateById = (id: string) => {
    return certificates.value.find((c) => c.id === id)
  }

  const addCertificate = (certificate: Certificate) => {
    certificates.value.push(certificate)
  }

  const updateCertificate = (id: string, updates: Partial<Certificate>) => {
    const index = certificates.value.findIndex((c) => c.id === id)
    if (index !== -1) {
      certificates.value[index] = { ...certificates.value[index], ...updates }
    }
  }

  const addTransaction = (transaction: Transaction) => {
    transactions.value.push(transaction)
  }

  const fetchCertificates = async () => {
    loading.value = true
    error.value = null
    try {
      await new Promise((resolve) => setTimeout(resolve, 500))
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Failed to fetch certificates"
    } finally {
      loading.value = false
    }
  }

  const fetchTransactions = async () => {
    loading.value = true
    error.value = null
    try {
      await new Promise((resolve) => setTimeout(resolve, 500))
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Failed to fetch transactions"
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    certificates,
    transactions,
    loading,
    error,
    activeCertificates,
    revokedCertificates,
    getCertificateById,
    addCertificate,
    updateCertificate,
    addTransaction,
    fetchCertificates,
    fetchTransactions,
    clearError,
  }
})
