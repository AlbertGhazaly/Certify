<template>
  <div class="group bg-gradient-to-r from-slate-800 to-slate-800/50 border border-slate-700 hover:border-purple-500/30 rounded-xl p-4 hover:shadow-lg hover:shadow-purple-500/5 transition-all duration-300">
    <!-- Header with Type and Time -->
    <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-700">
      <div class="flex items-center gap-3">
        <!-- Type Indicator Dot -->
        <div
          :class="[
            'w-3 h-3 rounded-full flex-shrink-0',
            typeColor
          ]"
        />
        <h3 class="font-bold text-white capitalize">{{ transaction.type }} Transaction</h3>
      </div>
      <span class="text-xs text-gray-500 whitespace-nowrap">{{ formatTime(transaction.timestamp) }}</span>
    </div>

    <!-- Transaction Details Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4 text-sm">
      <!-- Certificate ID -->
      <div class="space-y-1">
        <p class="text-xs text-gray-500 font-medium">Certificate ID</p>
        <p class="font-mono text-xs text-gray-400 truncate bg-slate-900/50 px-2 py-1.5 rounded">
          {{ transaction.certificateId }}
        </p>
      </div>

      <!-- Transaction Hash -->
      <div class="space-y-1">
        <p class="text-xs text-gray-500 font-medium">Tx Hash</p>
        <p class="font-mono text-xs text-gray-400 truncate bg-slate-900/50 px-2 py-1.5 rounded">
          {{ transaction.hash }}
        </p>
      </div>

      <!-- Issuer Address -->
      <div class="space-y-1">
        <p class="text-xs text-gray-500 font-medium">Issuer</p>
        <p class="font-mono text-xs text-gray-400 truncate bg-slate-900/50 px-2 py-1.5 rounded">
          {{ transaction.issuerAddress }}
        </p>
      </div>

      <!-- Block Number -->
      <div class="space-y-1">
        <p class="text-xs text-gray-500 font-medium">Block #</p>
        <p class="text-white font-semibold">{{ transaction.blockNumber }}</p>
      </div>
    </div>

    <!-- Signature Section -->
    <div class="pt-4 border-t border-slate-700">
      <p class="text-xs text-gray-500 font-medium mb-2">Signature</p>
      <div class="bg-slate-900/50 px-3 py-2 rounded border border-slate-700 hover:border-slate-600 transition">
        <p class="font-mono text-xs text-gray-500 truncate">
          {{ transaction.signature }}
        </p>
      </div>
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
