<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="max-w-4xl mx-auto px-4">
      <router-link to="/explorer" class="text-blue-600 hover:text-blue-700 mb-6 inline-block">
        ← Back to Explorer
      </router-link>

      <template v-if="isLoading">
        <div class="bg-white rounded-lg shadow-md p-8 text-center">
          <p class="text-gray-600">Loading certificate details...</p>
        </div>
      </template>

      <template v-else-if="!certificate">
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <p class="text-red-900">Certificate not found</p>
        </div>
      </template>

      <template v-else>
        <div class="bg-white rounded-lg shadow-md p-8 mb-8">
          <div class="mb-6 pb-6 border-b border-gray-200">
            <div class="flex items-start justify-between mb-4">
              <div>
                <h1 class="text-3xl font-bold text-gray-900">{{ certificate.studentName }}</h1>
                <p class="text-gray-600 mt-1">Student ID: {{ certificate.studentId }}</p>
              </div>
              <span
                :class="[
                  'px-4 py-2 rounded-full text-sm font-semibold',
                  certificate.status === 'active'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                ]"
              >
                {{ certificate.status.toUpperCase() }}
              </span>
            </div>
          </div>

          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-8 mb-8 border border-blue-200">
            <div class="text-center space-y-4">
              <p class="text-gray-700">Kementerian Pendidikan Tinggi, Sains, dan Teknologi</p>
              <p class="text-gray-700">{{ certificate.institution }}</p>
              <p class="text-gray-700 mt-6">Dengan ini menyatakan bahwa</p>
              <p class="text-2xl font-bold text-gray-900 mt-4">{{ certificate.studentName }}</p>
              <p class="text-gray-700">Telah menyelesaikan dan memenuhi semua persyaratan</p>
              <p class="text-lg font-semibold text-indigo-900 mt-4">{{ certificate.degree }}</p>
              <p class="text-gray-700 mt-6">Diberikan di {{ certificate.institution }}</p>
              <p class="text-gray-700">{{ formatDate(certificate.issueDate) }}</p>
            </div>
          </div>

          <div class="grid md:grid-cols-2 gap-6 mb-8">
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="font-semibold text-gray-900 mb-3">Issued By</h3>
              <p class="font-mono text-sm text-gray-700 break-all">{{ certificate.issuerAddress }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="font-semibold text-gray-900 mb-3">Issued Date</h3>
              <p class="text-gray-700">{{ formatDate(certificate.issueDate) }}</p>
            </div>
          </div>

          <div class="space-y-4 mb-8">
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="font-semibold text-gray-900 mb-2">Document Hash (SHA-256)</h3>
              <p class="font-mono text-xs text-gray-700 break-all bg-white p-2 rounded">
                {{ certificate.documentHash }}
              </p>
            </div>
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="font-semibold text-gray-900 mb-2">IPFS CID</h3>
              <p class="font-mono text-xs text-gray-700 break-all bg-white p-2 rounded">
                {{ certificate.ipfsCid }}
              </p>
            </div>
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="font-semibold text-gray-900 mb-2">Signature Hash</h3>
              <p class="font-mono text-xs text-gray-700 break-all bg-white p-2 rounded">
                {{ certificate.signatureHash }}
              </p>
            </div>
          </div>

          <div class="flex gap-4 pt-4 border-t border-gray-200">
            <button
              @click="downloadCertificate"
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition"
            >
              Download Certificate
            </button>
            <button
              @click="verifyCertificate"
              class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition"
            >
              Verify on Blockchain
            </button>
            <router-link
              :to="`/explorer?tx=${certificate.signatureHash}`"
              class="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg font-medium hover:bg-gray-700 transition text-center"
            >
              View on Explorer
            </router-link>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCertificateStore } from '@/stores/certificateStore'
import type { Certificate } from '@/types'

const route = useRoute()
const certificateStore = useCertificateStore()

const certificate = ref<Certificate | null>(null)
const isLoading = ref(true)

const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const downloadCertificate = () => {
  alert('Certificate download feature would be implemented with actual PDF generation')
}

const verifyCertificate = () => {
  alert('Certificate verification initiated')
}

onMounted(() => {
  const certificateId = route.params.id as string
  certificate.value = certificateStore.getCertificateById(certificateId)
  
  isLoading.value = false
})
</script>
