<template>
  <div class="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl border border-slate-700 hover:border-purple-500/50 shadow-lg hover:shadow-xl hover:shadow-purple-500/10 transition-all duration-300 p-6 overflow-hidden relative">
    <!-- Background Glow -->
    <div class="absolute inset-0 bg-gradient-to-br from-purple-500/0 via-transparent to-purple-500/0 group-hover:from-purple-500/5 group-hover:to-purple-500/5 transition-all duration-300" />

    <div class="relative z-10">
      <!-- Header with Status -->
      <div class="flex items-start justify-between gap-3 mb-4">
        <div class="flex-1 min-w-0">
          <h3 class="text-lg font-bold text-white truncate">{{ certificate.studentName }}</h3>
          <p class="text-xs text-gray-500 font-mono mt-1">ID: {{ certificate.studentId }}</p>
        </div>
        
        <!-- Status Badge -->
        <span
          :class="[
            'px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap flex-shrink-0',
            certificate.status === 'active'
              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
              : 'bg-red-500/20 text-red-300 border border-red-500/30'
          ]"
        >
          {{ certificate.status }}
        </span>
      </div>

      <!-- Certificate Details -->
      <div class="space-y-3 text-sm mb-5 pb-5 border-b border-slate-700">
        <div>
          <p class="text-xs text-gray-500 mb-1">Degree</p>
          <p class="text-white font-medium">{{ certificate.degree }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 mb-1">Institution</p>
          <p class="text-white font-medium">{{ certificate.institution }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 mb-1">Issue Date</p>
          <p class="text-white font-medium">{{ formatDate(certificate.issueDate) }}</p>
        </div>
      </div>

      <!-- Blockchain Info -->
      <div class="space-y-2 text-xs mb-5 pb-5 border-b border-slate-700">
        <div>
          <p class="text-gray-500 mb-1">Doc Hash</p>
          <p class="text-gray-400 font-mono truncate bg-slate-900/50 px-2 py-1 rounded">{{ certificate.documentHash }}</p>
        </div>
        <div>
          <p class="text-gray-500 mb-1">IPFS CID</p>
          <p class="text-gray-400 font-mono truncate bg-slate-900/50 px-2 py-1 rounded">{{ certificate.ipfsCid }}</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-3">
        <router-link
          :to="`/certificate/${certificate.id}`"
          class="flex-1 px-4 py-2.5 bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-600 text-white rounded-lg text-sm font-semibold transition-all duration-300 text-center"
        >
          View Details
        </router-link>
        <button
          @click="emit('verify')"
          class="flex-1 px-4 py-2.5 bg-slate-700/50 hover:bg-slate-700 text-gray-300 hover:text-white rounded-lg text-sm font-semibold transition-all duration-300 border border-slate-600"
        >
          Verify
        </button>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import type { Certificate } from '@/types';

defineProps<{
  certificate: Certificate;
}>();

const emit = defineEmits<{
  verify: [];
}>();

const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};
</script>
