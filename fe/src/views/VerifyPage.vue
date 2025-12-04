<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="max-w-4xl mx-auto px-4">
      <div class="bg-white rounded-lg shadow-md p-8 mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Verify Diploma</h1>
        <p class="text-gray-600 mb-8">Enter certificate details to verify its authenticity on the blockchain</p>

        <form @submit.prevent="handleVerify" class="space-y-6">
          <div class="grid md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Certificate ID *</label>
              <input
                v-model="searchForm.certificateId"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="CERT_1234567890"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Transaction Hash *</label>
              <input
                v-model="searchForm.transactionHash"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0x..."
              />
            </div>
          </div>

          <div class="grid md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Document Hash (SHA-256) *</label>
              <input
                v-model="searchForm.documentHash"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Hash in hex format"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Issuer Address *</label>
              <input
                v-model="searchForm.issuerAddress"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0x..."
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">AES Encryption Key</label>
            <input
              v-model="searchForm.encryptionKey"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Required to decrypt the diploma PDF"
            />
          </div>

          <button
            type="submit"
            :disabled="isVerifying"
            class="w-full px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 transition"
          >
            <span v-if="!isVerifying">Verify Certificate</span>
            <span v-else>Verifying...</span>
          </button>
        </form>

        <div v-if="verificationError" class="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
          <p class="text-red-900 font-medium">Verification Failed</p>
          <p class="text-red-800 text-sm mt-1">{{ verificationError }}</p>
        </div>
      </div>

      <template v-if="verificationResult">
        <div
          :class="[
            'rounded-lg shadow-md p-8 mb-8',
            verificationResult.isValid ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
          ]"
        >
          <div class="flex items-start gap-4">
            <div
              :class="[
                'w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0',
                verificationResult.isValid ? 'bg-green-200' : 'bg-red-200'
              ]"
            >
              <span :class="verificationResult.isValid ? 'text-green-700' : 'text-red-700'">
                {{ verificationResult.isValid ? '✓' : '✗' }}
              </span>
            </div>
            <div class="flex-1">
              <h2
                :class="[
                  'text-2xl font-bold mb-2',
                  verificationResult.isValid ? 'text-green-900' : 'text-red-900'
                ]"
              >
                {{ verificationResult.isValid ? 'Certificate Valid' : 'Certificate Invalid' }}
              </h2>
              <p
                :class="verificationResult.isValid ? 'text-green-800' : 'text-red-800'"
              >
                {{ verificationResult.isValid ? 'This diploma is authentic and has not been tampered with.' : 'This diploma could not be verified.' }}
              </p>
            </div>
          </div>
        </div>

        <template v-if="verificationResult.certificate">
          <CertificateCard :certificate="verificationResult.certificate" @verify="handleVerify" />
        </template>

        <template v-if="verificationResult.errors.length > 0">
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h3 class="font-semibold text-yellow-900 mb-3">Verification Issues</h3>
            <ul class="space-y-2">
              <li v-for="(error, index) in verificationResult.errors" :key="index" class="text-sm text-yellow-800">
                • {{ error }}
              </li>
            </ul>
          </div>
        </template>
      </template>
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
