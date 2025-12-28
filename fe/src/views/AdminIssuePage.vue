<template>
  <div class="min-h-screen bg-background py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <router-link
        to="/admin"
        class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8"
      >
        <span>←</span> Back
      </router-link>

      <!-- Issue Certificate Section -->
      <div class="bg-card border border-border rounded-xl p-6 sm:p-8 mb-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-foreground mb-2">Terbitkan Ijazah Baru</h1>
        <p class="text-muted-foreground mb-8">Buat dan terbitkan sertifikat ijazah digital</p>

        <form @submit.prevent="handleSubmit" class="space-y-8">
          <!-- Student Information -->
          <div>
            <h2 class="text-lg font-semibold text-foreground mb-4">Informasi Mahasiswa</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Nama Lengkap *</label>
                <input
                  v-model="form.studentName"
                  type="text"
                  required
                  placeholder="Nama lengkap mahasiswa"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">NIM *</label>
                <input
                  v-model="form.studentId"
                  type="text"
                  required
                  pattern="\d{8}"
                  placeholder="8 digit NIM"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
            </div>
          </div>

          <!-- Degree Information -->
          <div>
            <h2 class="text-lg font-semibold text-foreground mb-4">Informasi Program Studi</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Program Studi *</label>
                <input
                  v-model="form.degree"
                  type="text"
                  required
                  placeholder="e.g., Teknik Informatika"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Tanggal Diterbitkan *</label>
                <input
                  v-model="form.issueDate"
                  type="date"
                  required
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
            </div>
          </div>

          <!-- Birth Information -->
          <div>
            <h2 class="text-lg font-semibold text-foreground mb-4">Informasi Kelahiran</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Tempat Lahir *</label>
                <input
                  v-model="form.birthPlace"
                  type="text"
                  required
                  placeholder="Kota"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Tanggal Lahir *</label>
                <input
                  v-model="form.birthDate"
                  type="date"
                  required
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
            </div>
          </div>

          <!-- Issuers Selection -->
          <div>
            <h2 class="text-lg font-semibold text-foreground mb-4">Penerbit</h2>
            <div class="space-y-2">
              <label class="flex items-center gap-2">
                <input
                  type="checkbox"
                  v-model="form.requiresAllSignatures"
                  class="w-4 h-4 text-accent bg-background border-border rounded focus:ring-2 focus:ring-accent"
                />
                <span class="text-sm text-foreground">Memerlukan tanda tangan semua penerbit</span>
              </label>
              <p class="text-xs text-muted-foreground">
                Jika dicentang, semua penerbit harus menandatangani. Jika tidak, mayoritas sudah cukup.
              </p>
            </div>
          </div>

          <!-- Submit -->
          <div class="flex flex-col sm:flex-row gap-4 pt-4">
            <button
              type="submit"
              :disabled="isSubmitting"
              class="flex-1 px-6 py-3 bg-accent text-accent-foreground rounded-lg font-medium hover:bg-accent/90 disabled:bg-muted disabled:cursor-not-allowed transition"
            >
              {{ isSubmitting ? 'Memproses...' : 'Terbitkan Ijazah' }}
            </button>
            <button
              type="button"
              @click="resetForm"
              :disabled="isSubmitting"
              class="px-6 py-3 bg-secondary text-foreground rounded-lg font-medium hover:bg-secondary/80 disabled:opacity-50 transition"
            >
              Bersihkan
            </button>
          </div>

          <!-- Messages -->
          <div v-if="successMessage" class="bg-accent/10 border border-accent/50 rounded-lg p-4">
            <p class="text-accent font-semibold mb-2">✓ Berhasil!</p>
            <p class="text-sm text-foreground whitespace-pre-line">{{ successMessage }}</p>
            <div v-if="aesKey" class="mt-4 p-3 bg-background rounded border border-border">
              <p class="text-xs text-muted-foreground mb-1">Kunci AES (simpan dengan aman):</p>
              <code class="text-xs text-accent break-all">{{ aesKey }}</code>
            </div>
          </div>
          <div v-if="errorMessage" class="bg-destructive/10 border border-destructive/50 rounded-lg p-4 text-destructive">
            <p class="font-semibold mb-1">✗ Error</p>
            <p class="text-sm">{{ errorMessage }}</p>
          </div>
        </form>
      </div>

      <!-- Revoke Certificate Section -->
      <div class="bg-card border border-border rounded-xl p-6 sm:p-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-foreground mb-2">Cabut Ijazah</h1>
        <p class="text-muted-foreground mb-8">Cabut sertifikat ijazah yang sudah diterbitkan</p>

        <form @submit.prevent="handleRevoke" class="space-y-8">
          <!-- Revoke Information -->
          <div>
            <h2 class="text-lg font-semibold text-foreground mb-4">Informasi Pencabutan</h2>
            <div class="grid grid-cols-1 gap-4">
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">NIM *</label>
                <input
                  v-model="revokeForm.studentId"
                  type="text"
                  required
                  pattern="\d{8}"
                  placeholder="8 digit NIM yang akan dicabut"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Alasan Pencabutan *</label>
                <textarea
                  v-model="revokeForm.reason"
                  required
                  rows="3"
                  placeholder="Masukkan alasan pencabutan ijazah"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent resize-none"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Submit Revoke -->
          <div class="flex flex-col sm:flex-row gap-4 pt-4">
            <button
              type="submit"
              :disabled="isRevoking"
              class="flex-1 px-6 py-3 bg-destructive text-destructive-foreground rounded-lg font-medium hover:bg-destructive/90 disabled:bg-muted disabled:cursor-not-allowed transition"
            >
              {{ isRevoking ? 'Memproses...' : 'Cabut Ijazah' }}
            </button>
            <button
              type="button"
              @click="resetRevokeForm"
              :disabled="isRevoking"
              class="px-6 py-3 bg-secondary text-foreground rounded-lg font-medium hover:bg-secondary/80 disabled:opacity-50 transition"
            >
              Bersihkan
            </button>
          </div>

          <!-- Revoke Messages -->
          <div v-if="revokeSuccessMessage" class="bg-accent/10 border border-accent/50 rounded-lg p-4">
            <p class="text-accent font-semibold mb-2">✓ Berhasil!</p>
            <p class="text-sm text-foreground whitespace-pre-line">{{ revokeSuccessMessage }}</p>
          </div>
          <div v-if="revokeErrorMessage" class="bg-destructive/10 border border-destructive/50 rounded-lg p-4 text-destructive">
            <p class="font-semibold mb-1">✗ Error</p>
            <p class="text-sm">{{ revokeErrorMessage }}</p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import axios from 'axios'
import { CryptoUtils } from '@/utils/crypto'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const CONTRACT_ADDRESS = '0x0AcCEf6086E744608C2B342041C07a261196FF67'

const router = useRouter()
const authStore = useAuthStore()

// Issue form state
const form = ref({
  studentName: '',
  studentId: '',
  degree: '',
  issueDate: '',
  birthPlace: '',
  birthDate: '',
  requiresAllSignatures: true
})

const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const aesKey = ref('')

// Revoke form state
const revokeForm = ref({
  studentId: '',
  reason: ''
})

const isRevoking = ref(false)
const revokeSuccessMessage = ref('')
const revokeErrorMessage = ref('')

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const handleSubmit = async () => {
  if (!authStore.userAddress) {
    errorMessage.value = 'Anda harus login terlebih dahulu'
    return
  }

  isSubmitting.value = true
  errorMessage.value = ''
  successMessage.value = ''
  aesKey.value = ''

  try {
    console.log('Step 1: Generating certificate and uploading to IPFS...')
    
    // Step 1: Generate certificate and upload to IPFS
    const issueResponse = await axios.post(`${API_URL}/certificate/issue`, {
      student_name: form.value.studentName,
      student_id: form.value.studentId,
      degree: form.value.degree,
      birth_place: form.value.birthPlace,
      birth_date: formatDate(form.value.birthDate),
      issue_date: formatDate(form.value.issueDate),
      issuer_wallets: [authStore.userAddress],
      requires_all_signatures: form.value.requiresAllSignatures
    })

    if (!issueResponse.data.success) {
      throw new Error(issueResponse.data.message)
    }

    const { student_id, ipfs_cid, cert_hash, aes_key } = issueResponse.data
    aesKey.value = aes_key

    console.log('✓ Certificate prepared:', { student_id, ipfs_cid, cert_hash })

    // Step 2: Sign the certificate hash with MetaMask
    console.log('Step 2: Requesting signature from MetaMask...')
    const signature = await CryptoUtils.signWithMetaMask(cert_hash, authStore.userAddress)
    console.log('✓ Signature obtained:', signature.substring(0, 20) + '...')

    // Step 3: Submit to blockchain via MetaMask
    console.log('Step 3: Submitting to blockchain...')
    
    const CONTRACT_ABI = [
      {
        "inputs": [
          {"name": "studentId", "type": "string"},
          {"name": "certHash", "type": "bytes32"},
          {"name": "ipfsCID", "type": "string"},
          {"name": "issuerWallets", "type": "address[]"},
          {"name": "signature", "type": "bytes"},
          {"name": "requiresAllSignatures", "type": "bool"}
        ],
        "name": "proposeCertificate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      }
    ]

    // Convert hash to bytes32 (ensure proper format)
    const certHashBytes = '0x' + cert_hash

    console.log('Transaction parameters:', {
      studentId: student_id,
      certHash: certHashBytes,
      ipfsCID: ipfs_cid,
      issuerWallets: [authStore.userAddress],
      signature: signature.substring(0, 20) + '...',
      requiresAllSignatures: form.value.requiresAllSignatures
    })

    // Send transaction using the utility function
    const tx = await CryptoUtils.sendContractTransaction(
      CONTRACT_ADDRESS,
      CONTRACT_ABI,
      'proposeCertificate',
      [
        student_id,
        certHashBytes,
        ipfs_cid,
        [authStore.userAddress],
        signature,
        form.value.requiresAllSignatures
      ],
      authStore.userAddress
    )

    console.log('✓ Transaction successful:', tx.transactionHash)

    successMessage.value = `Ijazah berhasil diterbitkan untuk NIM ${student_id}!\n\nTransaction Hash: ${tx.transactionHash}\n\nIPFS CID: ${ipfs_cid}`
    
    // Reset form after 10 seconds
    setTimeout(() => {
      resetForm()
    }, 10000)

  } catch (e: any) {
    console.error('Error during certificate issuance:', e)
    
    if (e.code === 4001) {
      errorMessage.value = 'Transaksi dibatalkan oleh pengguna'
    } else if (e.message?.includes('MetaMask')) {
      errorMessage.value = e.message
    } else if (e.response?.data?.detail) {
      errorMessage.value = e.response.data.detail
    } else if (e.message) {
      errorMessage.value = e.message
    } else {
      errorMessage.value = 'Gagal menerbitkan ijazah. Silakan coba lagi.'
    }
  } finally {
    isSubmitting.value = false
  }
}

const handleRevoke = async () => {
  if (!authStore.userAddress) {
    revokeErrorMessage.value = 'Anda harus login terlebih dahulu'
    return
  }

  isRevoking.value = true
  revokeErrorMessage.value = ''
  revokeSuccessMessage.value = ''

  try {
    console.log('Step 1: Creating revocation signature message...')
    
    // Create message to sign for revocation
    const message = `Revoke certificate for student ${revokeForm.value.studentId}: ${revokeForm.value.reason}`
    
    // Step 2: Sign the revocation with MetaMask
    console.log('Step 2: Requesting revocation signature from MetaMask...')
    const signature = await CryptoUtils.signWithMetaMask(message, authStore.userAddress)
    console.log('✓ Revocation signature obtained:', signature.substring(0, 20) + '...')

    // Step 3: Submit revocation to blockchain
    console.log('Step 3: Submitting revocation to blockchain...')
    
    const REVOKE_ABI = [
      {
        "inputs": [
          {"name": "studentId", "type": "string"},
          {"name": "reason", "type": "string"},
          {"name": "signature", "type": "bytes"}
        ],
        "name": "signCertificateRevocation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      }
    ]

    console.log('Revocation parameters:', {
      studentId: revokeForm.value.studentId,
      reason: revokeForm.value.reason,
      signature: signature.substring(0, 20) + '...'
    })

    // Send revocation transaction
    const tx = await CryptoUtils.sendContractTransaction(
      CONTRACT_ADDRESS,
      REVOKE_ABI,
      'signCertificateRevocation',
      [
        revokeForm.value.studentId,
        revokeForm.value.reason,
        signature
      ],
      authStore.userAddress
    )

    console.log('✓ Revocation transaction successful:', tx.transactionHash)

    revokeSuccessMessage.value = `Ijazah untuk NIM ${revokeForm.value.studentId} berhasil dicabut!\n\nAlasan: ${revokeForm.value.reason}\n\nTransaction Hash: ${tx.transactionHash}`
    
    // Reset form after 10 seconds
    setTimeout(() => {
      resetRevokeForm()
    }, 10000)

  } catch (e: any) {
    console.error('Error during certificate revocation:', e)
    
    if (e.code === 4001) {
      revokeErrorMessage.value = 'Transaksi dibatalkan oleh pengguna'
    } else if (e.message?.includes('MetaMask')) {
      revokeErrorMessage.value = e.message
    } else if (e.message?.includes('not valid or already revoked')) {
      revokeErrorMessage.value = 'Sertifikat tidak valid atau sudah dicabut sebelumnya'
    } else if (e.message?.includes('not an authorized issuer')) {
      revokeErrorMessage.value = 'Anda tidak memiliki otorisasi untuk mencabut sertifikat ini'
    } else if (e.message?.includes('does not exist')) {
      revokeErrorMessage.value = 'Sertifikat tidak ditemukan untuk NIM tersebut'
    } else if (e.message) {
      revokeErrorMessage.value = e.message
    } else {
      revokeErrorMessage.value = 'Gagal mencabut ijazah. Silakan coba lagi.'
    }
  } finally {
    isRevoking.value = false
  }
}

const resetForm = () => {
  form.value = {
    studentName: '',
    studentId: '',
    degree: '',
    issueDate: '',
    birthPlace: '',
    birthDate: '',
    requiresAllSignatures: true
  }
  successMessage.value = ''
  errorMessage.value = ''
  aesKey.value = ''
}

const resetRevokeForm = () => {
  revokeForm.value = {
    studentId: '',
    reason: ''
  }
  revokeSuccessMessage.value = ''
  revokeErrorMessage.value = ''
}
</script>