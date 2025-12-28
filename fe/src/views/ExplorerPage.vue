<!-- eslint-disable vue/no-multiple-template-root -->
<template>
  <div class="min-h-screen bg-background py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <router-link to="/" class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-4">
          <span>←</span> Back
        </router-link>
        <h1 class="text-3xl sm:text-4xl font-bold text-foreground mb-2">Blockchain Explorer</h1>
        <p class="text-muted-foreground">View all diploma transactions</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-card border border-border rounded-lg p-4 sm:p-6">
          <p class="text-muted-foreground text-sm">Total Transactions</p>
          <p class="text-2xl sm:text-3xl font-bold text-foreground mt-2">{{ totalTransactions }}</p>
        </div>
        <div class="bg-card border border-border rounded-lg p-4 sm:p-6">
          <p class="text-muted-foreground text-sm">Issued Diplomas</p>
          <p class="text-2xl sm:text-3xl font-bold text-accent mt-2">{{ issuedCount }}</p>
        </div>
        <div class="bg-card border border-border rounded-lg p-4 sm:p-6">
          <p class="text-muted-foreground text-sm">Revoked</p>
          <p class="text-2xl sm:text-3xl font-bold text-destructive mt-2">{{ revokedCount }}</p>
        </div>
        <div class="bg-card border border-border rounded-lg p-4 sm:p-6">
          <p class="text-muted-foreground text-sm">Active</p>
          <p class="text-2xl sm:text-3xl font-bold text-accent mt-2">{{ activeDiplomasCount }}</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 mb-8">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">Type</label>
            <select
              v-model="filters.type"
              class="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            >
              <option value="">All Types</option>
              <option value="issue">Issue</option>
              <option value="revoke">Revoke</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">Status</label>
            <select
              v-model="filters.status"
              class="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            >
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="revoked">Revoked</option>
            </select>
          </div>
          <div class="sm:col-span-2 lg:col-span-1">
            <label class="block text-sm font-medium text-foreground mb-2">Search</label>
            <input
              v-model="filters.search"
              type="text"
              placeholder="ID or hash..."
              class="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            />
          </div>
          <button
            @click="resetFilters"
            class="text-accent hover:text-accent/80 font-medium text-sm self-end"
          >
            Reset
          </button>
        </div>
      </div>

      <!-- Transactions Table -->
      <div class="bg-card border border-border rounded-lg overflow-hidden">
        <!-- Loading State -->
        <div v-if="isLoading" class="p-8 text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-accent"></div>
          <p class="mt-4 text-muted-foreground">Loading certificates from blockchain...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="p-8 text-center">
          <p class="text-destructive mb-4">{{ error }}</p>
          <button
            @click="fetchCertificates"
            class="px-4 py-2 bg-accent text-white rounded-lg hover:bg-accent/80"
          >
            Retry
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="paginatedCertificates.length === 0" class="p-8 text-center">
          <p class="text-muted-foreground">No certificates found</p>
        </div>

        <!-- Table -->
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-border bg-secondary/50">
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase">Status</th>
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase">Student ID</th>
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase hidden md:table-cell">Certificate Hash</th>
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase hidden lg:table-cell">Issued</th>
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase hidden lg:table-cell">Last Updated</th>
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase hidden xl:table-cell">Revoke Reason</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-for="cert in paginatedCertificates" :key="cert.studentId" class="hover:bg-secondary/30 transition">
                <td class="px-4 sm:px-6 py-3">
                  <span 
                    :class="getStatusBadgeClass(cert.isValid)"
                    class="inline-block px-2 py-1 text-xs font-semibold rounded"
                  >
                    {{ cert.isValid ? 'ACTIVE' : 'REVOKED' }}
                  </span>
                </td>
                <td class="px-4 sm:px-6 py-3 text-sm text-accent font-mono">{{ cert.studentId }}</td>
                <td class="px-4 sm:px-6 py-3 text-sm text-muted-foreground font-mono hidden md:table-cell truncate" :title="cert.certHash">
                  {{ truncateHash(cert.certHash) }}
                </td>
                <td class="px-4 sm:px-6 py-3 text-sm text-muted-foreground hidden lg:table-cell" :title="formatTimestamp(cert.timestampIssued)">
                  {{ getTimeAgo(cert.timestampIssued) }}
                </td>
                <td class="px-4 sm:px-6 py-3 text-sm text-muted-foreground hidden lg:table-cell" :title="formatTimestamp(cert.timestampLastUpdated)">
                  {{ getTimeAgo(cert.timestampLastUpdated) }}
                </td>
                <td class="px-4 sm:px-6 py-3 text-sm text-muted-foreground hidden xl:table-cell truncate">
                  {{ cert.revokeReason || '-' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="!isLoading && !error && totalPages > 1" class="border-t border-border px-4 py-3 flex items-center justify-between">
          <div class="text-sm text-muted-foreground">
            Showing {{ startIndex + 1 }} to {{ Math.min(endIndex, filteredCertificates.length) }} of {{ filteredCertificates.length }} certificates
          </div>
          <div class="flex gap-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1 border border-border rounded hover:bg-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 border border-border rounded hover:bg-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getAllCertificatesFromBlockchain, type BlockchainCertificate } from '@/services/api'

const isLoading = ref(false)
const certificates = ref<BlockchainCertificate[]>([])
const error = ref<string | null>(null)
const currentPage = ref(1)
const pageSize = ref(10)

const filters = ref({
  type: '',
  status: '',
  search: '',
})

const totalTransactions = computed(() => certificates.value.length)
const issuedCount = computed(() => certificates.value.length)
const revokedCount = computed(() =>
  certificates.value.filter(cert => !cert.isValid).length
)
const activeDiplomasCount = computed(() => 
  certificates.value.filter(cert => cert.isValid).length
)

const filteredCertificates = computed(() => {
  return certificates.value.filter(cert => {
    // Filter by type (issue/revoke)
    if (filters.value.type === 'issue' && !cert.isValid) return false
    if (filters.value.type === 'revoke' && cert.isValid) return false
    
    // Filter by status
    if (filters.value.status === 'active' && !cert.isValid) return false
    if (filters.value.status === 'revoked' && cert.isValid) return false
    
    // Filter by search
    if (filters.value.search) {
      const search = filters.value.search.toLowerCase()
      if (!cert.studentId.toLowerCase().includes(search) &&
          !cert.certHash.toLowerCase().includes(search)) {
        return false
      }
    }
    return true
  })
})

const totalPages = computed(() => Math.ceil(filteredCertificates.value.length / pageSize.value))
const startIndex = computed(() => (currentPage.value - 1) * pageSize.value)
const endIndex = computed(() => startIndex.value + pageSize.value)
const paginatedCertificates = computed(() =>
  filteredCertificates.value.slice(startIndex.value, endIndex.value)
)

const truncateHash = (hash: string): string => {
  if (hash.length <= 12) return hash
  return `${hash.slice(0, 8)}...${hash.slice(-4)}`
}

const formatTimestamp = (timestamp: number): string => {
  if (!timestamp || timestamp === 0) return 'N/A'
  return new Date(timestamp * 1000).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getTimeAgo = (timestamp: number): string => {
  if (!timestamp || timestamp === 0) return 'N/A'
  const now = Math.floor(Date.now() / 1000)
  const diff = now - timestamp
  
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`
  if (diff < 2592000) return `${Math.floor(diff / 86400)} days ago`
  if (diff < 31536000) return `${Math.floor(diff / 2592000)} months ago`
  return `${Math.floor(diff / 31536000)} years ago`
}

const getStatusBadgeClass = (isValid: boolean) => {
  return isValid 
    ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
    : 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
}

const resetFilters = () => {
  filters.value = { type: '', status: '', search: '' }
  currentPage.value = 1
}

const fetchCertificates = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await getAllCertificatesFromBlockchain()
    certificates.value = response.certificates
  } catch (err: any) {
    error.value = err.message || 'Failed to fetch certificates from blockchain'
    console.error('Error fetching certificates:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchCertificates()
})
</script>
