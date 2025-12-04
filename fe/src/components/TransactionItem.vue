<template>
  <div class="bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition">
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-3">
        <div
          :class="[
            'w-2 h-2 rounded-full',
            typeColor
          ]"
        />
        <h3 class="font-semibold text-gray-900 capitalize">{{ transaction.type }} Transaction</h3>
      </div>
      <span class="text-xs text-gray-600">{{ formatTime(transaction.timestamp) }}</span>
    </div>

    <div class="grid md:grid-cols-2 gap-4 text-sm">
      <div>
        <p class="text-gray-600">Certificate ID</p>
        <p class="font-mono text-xs text-gray-900 truncate">{{ transaction.certificateId }}</p>
      </div>
      <div>
        <p class="text-gray-600">Transaction Hash</p>
        <p class="font-mono text-xs text-gray-900 truncate">{{ transaction.hash }}</p>
      </div>
      <div>
        <p class="text-gray-600">Issuer</p>
        <p class="font-mono text-xs text-gray-900 truncate">{{ transaction.issuerAddress }}</p>
      </div>
      <div>
        <p class="text-gray-600">Block #</p>
        <p class="font-semibold text-gray-900">{{ transaction.blockNumber }}</p>
      </div>
    </div>

    <div class="mt-3 pt-3 border-t border-gray-200">
      <p class="text-xs text-gray-600 mb-2">Signature</p>
      <p class="font-mono text-xs bg-gray-50 p-2 rounded truncate text-gray-900">
        {{ transaction.signature }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Transaction } from '@/types';

const props = defineProps<{
  transaction: Transaction;
}>();

const typeColor = computed(() => {
  switch (props.transaction.type) {
    case 'issue':
      return 'bg-green-500';
    case 'revoke':
      return 'bg-red-500';
    case 'update':
      return 'bg-blue-500';
    default:
      return 'bg-gray-500';
  }
});

const formatTime = (timestamp: string): string => {
  return new Date(timestamp).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
</script>
