<!-- eslint-disable vue/no-multiple-template-root -->
<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="max-w-6xl mx-auto px-4">
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Blockchain Explorer</h1>
        <p class="text-gray-600">View all diploma issuance and revocation transactions</p>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <div class="grid md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Transaction Type</label>
            <select
              v-model="filters.type"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Types</option>
              <option value="issue">Issue</option>
              <option value="revoke">Revoke</option>
              <option value="update">Update</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select
              v-model="filters.status"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="revoked">Revoked</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Search</label>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Certificate ID or hash..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Results per page</label>
            <select
              v-model.number="pageSize"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="10">10</option>
              <option value="25">25</option>
              <option value="50">50</option>
            </select>
          </div>
        </div>
        <button
          @click="resetFilters"
          class="text-blue-600 hover:text-blue-700 text-sm font-medium"
        >
          Reset Filters
        </button>
      </div>

      <div class="grid md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white rounded-lg shadow-md p-6">
          <p class="text-gray-600 text-sm">Total Transactions</p>
          <p class="text-3xl font-bold text-gray-900 mt-2">{{ totalTransactions }}</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-6">
          <p class="text-gray-600 text-sm">Issued Diplomas</p>
          <p class="text-3xl font-bold text-green-600 mt-2">{{ issuedCount }}</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-6">
          <p class="text-gray-600 text-sm">Revoked Diplomas</p>
          <p class="text-3xl font-bold text-red-600 mt-2">{{ revokedCount }}</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-6">
          <p class="text-gray-600 text-sm">Active Diplomas</p>
          <p class="text-3xl font-bold text-blue-600 mt-2">{{ activeDiplomasCount }}</p>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <template v-if="isLoading">
          <div class="p-8 text-center">
            <p class="text-gray-600">Loading transactions...</p>
          </div>
        </template>

        <template v-else-if="filteredTransactions.length === 0">
          <div class="p-8 text-center">
            <p class="text-gray-600">No transactions found</p>
          </div>
        </template>

        <template v-else>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Type</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Certificate ID</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Block #</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Issuer</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Timestamp</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Hash</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr
                  v-for="transaction in paginatedTransactions"
                  :key="transaction.id"
                  class="hover:bg-gray-50 transition"
                >
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      :class="[
                        'px-2 py-1 text-xs font-semibold rounded',
                        getTransactionTypeClass(transaction.type)
                      ]"
                    >
                      {{ transaction.type.toUpperCase() }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <router-link
                      :to="`/certificate/${transaction.certificateId}`"
                      class="text-blue-600 hover:text-blue-700 font-mono text-sm"
                    >
                      {{ transaction.certificateId }}
                    </router-link>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    #{{ transaction.blockNumber }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    <span class="font-mono">{{ truncateAddress(transaction.issuerAddress) }}</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {{ formatTime(transaction.timestamp) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="font-mono text-xs text-gray-600 truncate block max-w-xs">
                      {{ transaction.hash }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <button
                      @click="viewTransactionDetails(transaction)"
                      class="text-blue-600 hover:text-blue-700 font-medium text-sm"
                    >
                      View
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
            <p class="text-sm text-gray-600">
              Showing {{ startIndex + 1 }} to {{ Math.min(endIndex, filteredTransactions.length) }} of {{ filteredTransactions.length }}
            </p>
            <div class="flex gap-2">
              <button
                @click="currentPage--"
                :disabled="currentPage === 1"
                class="px-3 py-1 border border-gray-300 rounded text-sm font-medium disabled:opacity-50"
              >
                Previous
              </button>
              <span class="px-3 py-1 text-sm font-medium">
                Page {{ currentPage }} of {{ totalPages }}
              </span>
              <button
                @click="currentPage++"
                :disabled="currentPage === totalPages"
                class="px-3 py-1 border border-gray-300 rounded text-sm font-medium disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        </template>
      </div>

      <template v-if="selectedTransaction">
        <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-96 overflow-y-auto">
            <div class="p-6 border-b border-gray-200 flex items-center justify-between">
              <h2 class="text-xl font-bold">Transaction Details</h2>
              <button @click="selectedTransaction = null" class="text-gray-500 hover:text-gray-700">
                ✕
              </button>
            </div>
            <TransactionItem :transaction="selectedTransaction" />
            <div class="p-6 border-t border-gray-200 flex gap-3">
              <router-link
                :to="`/certificate/${selectedTransaction.certificateId}`"
                class="flex-1 px-4 py-2 bg-blue-600 text-white rounded text-center font-medium hover:bg-blue-700"
              >
                View Certificate
              </router-link>
              <button
                @click="selectedTransaction = null"
                class="flex-1 px-4 py-2 bg-gray-200 text-gray-900 rounded font-medium hover:bg-gray-300"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </template>
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
