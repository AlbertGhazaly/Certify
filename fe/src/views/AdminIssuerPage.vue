<template>
  <div class="min-h-screen bg-background py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <router-link
        to="/admin"
        class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8"
      >
        ← Back
      </router-link>

      <div class="bg-card border border-border rounded-xl p-6 sm:p-8">
        <!-- Header -->
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-foreground mb-2">
            Issuer Registration Management
          </h1>
          <p class="text-muted-foreground">
            Review, approve, reject, or delete issuer registrations
          </p>
        </div>

        <!-- Filters -->
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
          <input
            v-model="filters.name"
            @input="fetchRegistrations"
            placeholder="Search name..."
            class="px-4 py-2 bg-background border border-border rounded-lg"
          />

          <select
            v-model="filters.status"
            @change="fetchRegistrations"
            class="px-4 py-2 bg-background border border-border rounded-lg"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="accept">Accepted</option>
            <option value="reject">Rejected</option>
          </select>

          <select
            v-model="filters.sort"
            @change="fetchRegistrations"
            class="px-4 py-2 bg-background border border-border rounded-lg"
          >
            <option value="latest">Latest</option>
            <option value="oldest">Oldest</option>
          </select>

          <button
            @click="clearFilters"
            class="px-4 py-2 bg-secondary rounded-lg"
          >
            Clear
          </button>
        </div>

        <!-- Bulk Actions -->
        <div
          v-if="selectedIds.length > 0"
          class="flex gap-3 mb-4"
        >
          <button
            @click="bulkAccept"
            class="px-4 py-2 bg-green-600 text-white rounded-lg"
          >
            Accept Selected
          </button>
          <button
            @click="bulkReject"
            class="px-4 py-2 bg-yellow-600 text-white rounded-lg"
          >
            Reject Selected
          </button>
          <button
            @click="bulkDelete"
            class="px-4 py-2 bg-destructive text-destructive-foreground rounded-lg"
          >
            Delete Selected
          </button>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="py-12 text-center text-muted-foreground">
          Loading issuer registrations...
        </div>

        <!-- Table -->
        <div v-else-if="items.length > 0" class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-border">
                <th class="px-3 py-3">
                  <input
                    type="checkbox"
                    :checked="allSelected"
                    @change="toggleSelectAll"
                  />
                </th>
                <th class="px-4 py-3 text-left">Name</th>
                <th class="px-4 py-3 text-left">Wallet</th>
                <th class="px-4 py-3 text-left">Status</th>
                <th class="px-4 py-3 text-left">Created</th>
                <th class="px-4 py-3 text-left">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="reg in items"
                :key="reg.id_registration"
                class="border-b border-border hover:bg-accent/5"
              >
                <td class="px-3 py-3">
                  <input
                    type="checkbox"
                    :value="reg.id_registration"
                    v-model="selectedIds"
                  />
                </td>
                <td class="px-4 py-3">{{ reg.name }}</td>
                <td class="px-4 py-3 font-mono text-sm">
                  {{ reg.wallet_address }}
                </td>
                <td class="px-4 py-3">
                  <span
                    :class="statusClass(reg.status)"
                    class="px-2 py-1 rounded text-xs font-medium"
                  >
                    {{ reg.status }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  {{ formatDate(reg.created_at) }}
                </td>
                <td class="px-4 py-3 flex gap-2">
                  <button
                    v-if="reg.status === 'pending'"
                    @click="acceptOne(reg.id_registration)"
                    class="px-3 py-1 bg-green-600 text-white rounded text-sm"
                  >
                    Accept
                  </button>
                  <button
                    v-if="reg.status === 'pending'"
                    @click="rejectOne(reg.id_registration)"
                    class="px-3 py-1 bg-yellow-600 text-white rounded text-sm"
                  >
                    Reject
                  </button>
                  <button
                    @click="deleteOne(reg.id_registration)"
                    class="px-3 py-1 bg-destructive text-destructive-foreground rounded text-sm"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div class="flex justify-between items-center mt-6">
            <p class="text-sm text-muted-foreground">
              Page {{ page }} of {{ totalPages }}
            </p>
            <div class="flex gap-2">
              <button
                @click="prevPage"
                :disabled="page === 1"
                class="px-3 py-2 bg-secondary rounded-lg"
              >
                Prev
              </button>
              <button
                @click="nextPage"
                :disabled="page >= totalPages"
                class="px-3 py-2 bg-secondary rounded-lg"
              >
                Next
              </button>
            </div>
          </div>
        </div>

        <!-- Empty -->
        <div v-else class="text-center py-12 text-muted-foreground">
          No issuer registrations found.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import {
  getIssuerRegistrations,
  acceptIssuerRegistration,
  rejectIssuerRegistration,
  deleteIssuerRegistration,
} from '@/services/api';
import type { IssuerRegistration } from '@/types';

const items = ref<IssuerRegistration[]>([]);
const isLoading = ref(false);

const page = ref(1);
const pageSize = 10;
const total = ref(0);

const filters = ref({
  name: '',
  status: '',
  sort: 'latest',
});

const selectedIds = ref<string[]>([]);

const totalPages = computed(() =>
  Math.ceil(total.value / pageSize)
);

const allSelected = computed(
  () =>
    items.value.length > 0 &&
    selectedIds.value.length === items.value.length
);

onMounted(fetchRegistrations);

async function fetchRegistrations() {
  isLoading.value = true;
  selectedIds.value = [];

  const params: Record<string, any> = {
    page: page.value,
    page_size: pageSize,
  };

  if (filters.value.name?.trim()) {
    params.name = filters.value.name;
  }

  if (filters.value.status) {
    params.status = filters.value.status;
  }

  if (filters.value.sort) {
    params.sort = filters.value.sort;
  }

  const res = await getIssuerRegistrations(params);

  items.value = res.items;
  total.value = res.total;
  isLoading.value = false;
}

function toggleSelectAll(e: Event) {
  const checked = (e.target as HTMLInputElement).checked;
  selectedIds.value = checked
    ? items.value.map(i => i.id_registration)
    : [];
}

function statusClass(status: string) {
  return {
    pending: 'bg-yellow-500/20 text-yellow-700',
    accept: 'bg-green-500/20 text-green-700',
    reject: 'bg-red-500/20 text-red-700',
  }[status];
}

function formatDate(ts: number) {
  return new Date(ts * 1000).toLocaleString();
}

async function acceptOne(id: string) {
  await acceptIssuerRegistration(id);
  fetchRegistrations();
}

async function rejectOne(id: string) {
  await rejectIssuerRegistration(id);
  fetchRegistrations();
}

async function deleteOne(id: string) {
  await deleteIssuerRegistration(id);
  fetchRegistrations();
}

async function bulkAccept() {
  await Promise.all(selectedIds.value.map(acceptIssuerRegistration));
  fetchRegistrations();
}

async function bulkReject() {
  await Promise.all(selectedIds.value.map(rejectIssuerRegistration));
  fetchRegistrations();
}

async function bulkDelete() {
  await Promise.all(selectedIds.value.map(deleteIssuerRegistration));
  fetchRegistrations();
}

function nextPage() {
  if (page.value < totalPages.value) {
    page.value++;
    fetchRegistrations();
  }
}

function prevPage() {
  if (page.value > 1) {
    page.value--;
    fetchRegistrations();
  }
}

function clearFilters() {
  filters.value = { name: '', status: '', sort: 'latest' };
  page.value = 1;
  fetchRegistrations();
}
</script>
