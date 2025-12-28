<template>
  <div class="min-h-screen bg-background py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <router-link
        to="/admin"
        class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8"
      >
        <span>←</span> Back
      </router-link>

      <div class="bg-card border border-border rounded-xl p-6 sm:p-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-foreground mb-2">Sign Certificate Issuance</h1>
        <p class="text-muted-foreground mb-8">Tanda tangani penerbitan sertifikat dengan wallet Anda</p>

        <!-- Search Certificate -->
        <div class="mb-8">
          <h2 class="text-lg font-semibold text-foreground mb-4">Cari Sertifikat</h2>
          <div class="flex gap-3">
            <input
              v-model="searchStudentId"
              type="text"
              placeholder="Masukkan Student ID / NIM"
              class="flex-1 px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            />
            <button
              @click="searchCertificate"
              :disabled="isSearching || !searchStudentId"
              class="px-6 py-2 bg-accent text-white rounded-lg hover:bg-accent/80 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {{ isSearching ? 'Searching...' : 'Search' }}
            </button>
          </div>
        </div>

        <!-- Certificate Details -->
        <div v-if="certificateData" class="mb-8 p-6 bg-secondary/30 border border-border rounded-lg">
          <h2 class="text-lg font-semibold text-foreground mb-4">Certificate Details</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
            <div>
              <p class="text-muted-foreground">Student ID</p>
              <p class="text-foreground font-mono">{{ certificateData.studentId }}</p>
            </div>
            <div>
              <p class="text-muted-foreground">Status</p>
              <span 
                :class="certificateData.isValid ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' : 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'"
                class="inline-block px-2 py-1 text-xs font-semibold rounded"
              >
                {{ certificateData.isValid ? 'Valid' : 'Revoked' }}
              </span>
            </div>
            <div>
              <p class="text-muted-foreground">Certificate Hash</p>
              <p class="text-foreground font-mono text-xs break-all">{{ certificateData.certHash }}</p>
            </div>
            <div>
              <p class="text-muted-foreground">IPFS CID</p>
              <p class="text-foreground font-mono text-xs break-all">{{ certificateData.ipfsCID || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-muted-foreground">Issued At</p>
              <p class="text-foreground">{{ formatTimestamp(certificateData.timestampIssued) }}</p>
            </div>
            <div>
              <p class="text-muted-foreground">Last Updated</p>
              <p class="text-foreground">{{ formatTimestamp(certificateData.timestampLastUpdated) }}</p>
            </div>
            <div class="sm:col-span-2">
              <p class="text-muted-foreground">Issue Signature Count</p>
              <p class="text-foreground">{{ certificateData.issueSignatureCount }} / {{ certificateData.issuerWallets?.length || 0 }} issuers</p>
            </div>
          </div>
        </div>

        <!-- Sign Form -->
        <form v-if="certificateData" @submit.prevent="handleSign" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">Student ID</label>
            <input
              v-model="form.studentId"
              type="text"
              readonly
              class="w-full px-4 py-2 bg-secondary/50 border border-border rounded-lg text-foreground cursor-not-allowed"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-foreground mb-2">
              Signature 
              <span class="text-xs text-muted-foreground ml-2">(akan di-generate otomatis dari wallet Anda)</span>
            </label>
            <textarea
              v-model="form.signature"
              rows="4"
              readonly
              placeholder="Signature akan muncul di sini setelah Anda sign dengan wallet"
              class="w-full px-4 py-2 bg-secondary/50 border border-border rounded-lg text-foreground font-mono text-xs resize-none cursor-not-allowed"
            ></textarea>
          </div>

          <div class="flex gap-4">
            <button
              type="button"
              @click="generateSignature"
              :disabled="isGenerating || !certificateData"
              class="flex-1 px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
            >
              {{ isGenerating ? 'Generating...' : 'Generate Signature' }}
            </button>
            <button
              type="submit"
              :disabled="isSigning || !form.signature"
              class="flex-1 px-6 py-3 bg-accent text-white rounded-lg hover:bg-accent/80 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
            >
              {{ isSigning ? 'Signing...' : 'Sign Certificate Issuance' }}
            </button>
          </div>
        </form>

        <!-- Success Message -->
        <div v-if="successMessage" class="mt-6 p-4 bg-green-100 dark:bg-green-900/30 border border-green-300 dark:border-green-700 rounded-lg">
          <p class="text-green-800 dark:text-green-300">{{ successMessage }}</p>
          <p v-if="txHash" class="text-sm text-green-700 dark:text-green-400 mt-2 font-mono break-all">
            Transaction: {{ txHash }}
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="mt-6 p-4 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg">
          <p class="text-red-800 dark:text-red-300">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { CryptoUtils } from '@/utils/crypto'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const CONTRACT_ADDRESS = '0x0AcCEf6086E744608C2B342041C07a261196FF67'

const authStore = useAuthStore()

const searchStudentId = ref('')
const isSearching = ref(false)
const certificateData = ref<any>(null)

const form = ref({
  studentId: '',
  signature: '',
  certHash: ''
})

const isGenerating = ref(false)
const isSigning = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const txHash = ref('')

const CONTRACT_ABI = [
  {
    "inputs": [
      {"name": "studentId", "type": "string"},
      {"name": "signature", "type": "bytes"}
    ],
    "name": "signCertificateIssuance",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]

const formatTimestamp = (timestamp: number): string => {
  if (!timestamp || timestamp === 0) return 'N/A'
  return new Date(timestamp * 1000).toLocaleString('id-ID', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const searchCertificate = async () => {
  isSearching.value = true
  errorMessage.value = ''
  successMessage.value = ''
  certificateData.value = null
  form.value.signature = ''
  
  try {
    console.log('Step 1: Fetching certificate data from backend...')
    
    const response = await axios.post(`${API_URL}/certificate/sign/prepare`, {
      student_id: searchStudentId.value
    })

    if (!response.data.success) {
      throw new Error(response.data.message || 'Failed to fetch certificate data')
    }

    const certData = response.data.certificate_data
    
    certificateData.value = {
      studentId: certData.studentId,
      certHash: certData.certHash,
      ipfsCID: certData.ipfsCID,
      issuerWallets: certData.issuerWallets,
      issueSignatureCount: certData.issueSignatureCount,
      revokeSignatureCount: certData.revokeSignatureCount,
      isValid: certData.isValid,
      timestampIssued: certData.timestampIssued,
      timestampLastUpdated: certData.timestampLastUpdated,
      revokeReason: certData.revokeReason,
      requiresAllSignatures: certData.requiresAllSignatures
    }
    
    form.value.studentId = searchStudentId.value
    form.value.certHash = response.data.cert_hash
    
    console.log('✓ Certificate data loaded:', certificateData.value)
    
  } catch (error: any) {
    console.error('Error searching certificate:', error)
    if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = error.message || 'Failed to search certificate'
    }
  } finally {
    isSearching.value = false
  }
}

const generateSignature = async () => {
  isGenerating.value = true
  errorMessage.value = ''
  
  try {
    if (!authStore.userAddress) {
      throw new Error('Please connect your wallet first')
    }

    console.log('Step 2: Generating signature with MetaMask...')
    
    const signature = await CryptoUtils.signWithMetaMask(
      form.value.certHash,
      authStore.userAddress
    )
    
    form.value.signature = signature
    console.log('✓ Signature generated:', signature.substring(0, 20) + '...')
    
  } catch (error: any) {
    console.error('Error generating signature:', error)
    if (error.code === 4001) {
      errorMessage.value = 'Signature request rejected by user'
    } else {
      errorMessage.value = error.message || 'Failed to generate signature'
    }
  } finally {
    isGenerating.value = false
  }
}

const handleSign = async () => {
  isSigning.value = true
  errorMessage.value = ''
  successMessage.value = ''
  txHash.value = ''
  
  try {
    if (!authStore.userAddress) {
      throw new Error('Please connect your wallet first')
    }

    console.log('Step 3: Submitting signature to blockchain...')
    
    const tx = await CryptoUtils.sendContractTransaction(
      CONTRACT_ADDRESS,
      CONTRACT_ABI,
      'signCertificateIssuance',
      [form.value.studentId, form.value.signature],
      authStore.userAddress
    )
    
    console.log('✓ Transaction successful:', tx.transactionHash)
    
    txHash.value = tx.transactionHash
    successMessage.value = 'Certificate issuance signed successfully!'
    
    setTimeout(() => {
      searchCertificate()
    }, 2000)
    
  } catch (error: any) {
    console.error('Error signing certificate:', error)
    if (error.code === 4001) {
      errorMessage.value = 'Transaction rejected by user'
    } else if (error.message) {
      errorMessage.value = error.message
    } else {
      errorMessage.value = 'Failed to sign certificate issuance'
    }
  } finally {
    isSigning.value = false
  }
}
</script>
