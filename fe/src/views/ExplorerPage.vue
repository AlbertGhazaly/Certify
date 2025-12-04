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
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-border bg-secondary/50">
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase">Type</th>
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase">ID</th>
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase hidden sm:table-cell">Block</th>
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase hidden md:table-cell">Issuer</th>
                <th class="px-4 sm:px-6 py-3 text-left text-xs font-semibold text-foreground uppercase hidden lg:table-cell">Timestamp</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-for="i in 5" :key="i" class="hover:bg-secondary/30 transition">
                <td class="px-4 sm:px-6 py-3">
                  <span class="inline-block px-2 py-1 bg-accent/20 text-accent text-xs font-semibold rounded">
                    {{ i % 2 === 0 ? 'ISSUE' : 'REVOKE' }}
                  </span>
                </td>
                <td class="px-4 sm:px-6 py-3 text-sm text-accent font-mono truncate">CERT_{{ String(1000000 + i).slice(-6) }}</td>
                <td class="px-4 sm:px-6 py-3 text-sm text-foreground hidden sm:table-cell">#{{ 50000 + i }}</td>
                <td class="px-4 sm:px-6 py-3 text-sm text-muted-foreground font-mono hidden md:table-cell truncate">0x1234...abcd</td>
                <td class="px-4 sm:px-6 py-3 text-sm text-muted-foreground hidden lg:table-cell">2 days ago</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCertificateStore } from '@/stores/certificateStore'
import type { Transaction } from '@/types'
import TransactionItem from '@/components/TransactionItem.vue'

const certificateStore = useCertificateStore()
const isLoading = ref(false)
const selectedTransaction = ref<Transaction | null>(null)
const currentPage = ref(1)
const pageSize = ref(10)

const filters = ref({
  type: '',
  status: '',
  search: '',
})

const totalTransactions = computed(() => certificateStore.transactions.length)
const issuedCount = computed(() =>
  certificateStore.transactions.filter(t => t.type === 'issue').length
)
const revokedCount = computed(() =>
  certificateStore.transactions.filter(t => t.type === 'revoke').length
)
const activeDiplomasCount = computed(() => certificateStore.activeCertificates.length)

const filteredTransactions = computed(() => {
  return certificateStore.transactions.filter(tx => {
    if (filters.value.type && tx.type !== filters.value.type) return false
    if (filters.value.search) {
      const search = filters.value.search.toLowerCase()
      if (!tx.certificateId.toLowerCase().includes(search) &&
          !tx.hash.toLowerCase().includes(search)) {
        return false
      }
    }
    return true
  })
})

const totalPages = computed(() => Math.ceil(filteredTransactions.value.length / pageSize.value))
const startIndex = computed(() => (currentPage.value - 1) * pageSize.value)
const endIndex = computed(() => startIndex.value + pageSize.value)
const paginatedTransactions = computed(() =>
  filteredTransactions.value.slice(startIndex.value, endIndex.value)
)

const truncateAddress = (address: string): string => {
  return `${address.slice(0, 6)}...${address.slice(-4)}`
}

const formatTime = (timestamp: string): string => {
  return new Date(timestamp).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getTransactionTypeClass = (type: string) => {
  switch (type) {
    case 'issue':
      return 'bg-green-100 text-green-800'
    case 'revoke':
      return 'bg-red-100 text-red-800'
    case 'update':
      return 'bg-blue-100 text-blue-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const viewTransactionDetails = (transaction: Transaction) => {
  selectedTransaction.value = transaction
}

const resetFilters = () => {
  filters.value = { type: '', status: '', search: '' }
  currentPage.value = 1
}

onMounted(() => {
  certificateStore.fetchTransactions()
})
</script>
