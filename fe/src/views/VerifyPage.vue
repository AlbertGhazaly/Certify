<template>
  <div class="min-h-screen bg-background py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <router-link to="/" class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8">
        <span>←</span> Back
      </router-link>

      <div class="bg-card border border-border rounded-xl p-6 sm:p-8 mb-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-foreground mb-2">Verify Diploma</h1>
        <p class="text-muted-foreground mb-8">Enter certificate details to verify its authenticity on the blockchain</p>

        <form @submit.prevent="handleVerify" class="space-y-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-foreground mb-2">Certificate ID *</label>
              <input
                v-model="searchForm.certificateId"
                type="text"
                required
                placeholder="CERT_1234567890"
                class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-foreground mb-2">Transaction Hash *</label>
              <input
                v-model="searchForm.transactionHash"
                type="text"
                required
                placeholder="0x..."
                class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-foreground mb-2">Document Hash (SHA-256) *</label>
              <input
                v-model="searchForm.documentHash"
                type="text"
                required
                placeholder="Hash in hex..."
                class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-foreground mb-2">Issuer Address *</label>
              <input
                v-model="searchForm.issuerAddress"
                type="text"
                required
                placeholder="0x..."
                class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-foreground mb-2">AES Encryption Key</label>
            <input
              v-model="searchForm.encryptionKey"
              type="password"
              placeholder="Leave blank if not encrypted"
              class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            />
          </div>

          <button
            type="submit"
            :disabled="isVerifying"
            class="w-full px-6 py-3 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 disabled:bg-muted transition"
          >
            {{ isVerifying ? 'Verifying...' : 'Verify Certificate' }}
          </button>
        </form>

        <div v-if="verificationError" class="mt-6 bg-destructive/10 border border-destructive/50 rounded-lg p-4">
          <p class="text-destructive font-medium">Verification Failed</p>
          <p class="text-destructive/80 text-sm mt-1">{{ verificationError }}</p>
        </div>
      </div>

      <div v-if="verificationResult" class="bg-card border border-border rounded-xl p-6 sm:p-8"
        :class="verificationResult.isValid ? 'border-accent/50' : 'border-destructive/50'"
      >
        <div class="flex items-start gap-4 mb-6">
          <div
            :class="[
              'w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 text-xl',
              verificationResult.isValid 
                ? 'bg-accent/20 text-accent' 
                : 'bg-destructive/20 text-destructive'
            ]"
          >
            {{ verificationResult.isValid ? '✓' : '✗' }}
          </div>
          <div>
            <h2
              :class="[
                'text-2xl font-bold mb-1',
                verificationResult.isValid ? 'text-accent' : 'text-destructive'
              ]"
            >
              {{ verificationResult.isValid ? 'Certificate Valid' : 'Certificate Invalid' }}
            </h2>
            <p :class="verificationResult.isValid ? 'text-accent/80' : 'text-destructive/80'">
              {{ verificationResult.isValid 
                ? 'This diploma is authentic and has not been tampered with.' 
                : 'This diploma could not be verified.' 
              }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useBlockchain } from '@/composables/useBlockchain'
import { Validators } from '@/utils/validators'
import type { VerificationResult } from '@/types'
import CertificateCard from '@/components/CertificateCard.vue'

const searchForm = ref({
  certificateId: '',
  transactionHash: '',
  documentHash: '',
  issuerAddress: '',
  encryptionKey: '',
})

const verificationResult = ref<VerificationResult | null>(null)
const verificationError = ref('')
const { verifyCertificate, isLoading: isVerifying } = useBlockchain()

const handleVerify = async () => {
  const errors = []
  
  if (!searchForm.value.certificateId.trim()) errors.push('Certificate ID is required')
  if (!searchForm.value.transactionHash.trim()) errors.push('Transaction hash is required')
  if (!Validators.isValidHash(searchForm.value.documentHash)) errors.push('Invalid document hash format')
  if (!Validators.isValidEthereumAddress(searchForm.value.issuerAddress)) {
    errors.push('Invalid issuer address format')
  }

  if (errors.length > 0) {
    verificationError.value = errors.join(', ')
    return
  }

  verificationError.value = ''
  verificationResult.value = null

  const isValid = await verifyCertificate(
    searchForm.value.certificateId,
    searchForm.value.transactionHash
  )

  verificationResult.value = {
    isValid,
    certificate: isValid ? {
      id: searchForm.value.certificateId,
      studentName: 'Rivaldo Thamrin Nasution',
      studentId: '11223029',
      institution: 'Institut Teknologi Bandung',
      degree: 'Sarjana Teknik',
      issueDate: new Date().toISOString(),
      signatureHash: searchForm.value.transactionHash,
      documentHash: searchForm.value.documentHash,
      ipfsCid: 'Qm...',
      issuerAddress: searchForm.value.issuerAddress,
      status: 'active',
      createdAt: new Date().toISOString(),
    } : null,
    errors: isValid ? [] : ['Certificate not found on blockchain'],
  }
}
</script>
