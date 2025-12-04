<template>
  <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
    <div class="flex items-start justify-between mb-4">
      <div>
        <h3 class="text-lg font-semibold text-gray-900">{{ certificate.studentName }}</h3>
        <p class="text-sm text-gray-600">ID: {{ certificate.studentId }}</p>
      </div>
      <span
        :class="[
          'px-3 py-1 rounded-full text-xs font-semibold',
          certificate.status === 'active'
            ? 'bg-green-100 text-green-800'
            : 'bg-red-100 text-red-800'
        ]"
      >
        {{ certificate.status }}
      </span>
    </div>

    <div class="space-y-2 text-sm mb-4 pb-4 border-b border-gray-200">
      <p><span class="font-medium text-gray-700">Degree:</span> {{ certificate.degree }}</p>
      <p><span class="font-medium text-gray-700">Institution:</span> {{ certificate.institution }}</p>
      <p><span class="font-medium text-gray-700">Issue Date:</span> {{ formatDate(certificate.issueDate) }}</p>
    </div>

    <div class="space-y-2 text-xs text-gray-600 mb-4">
      <p class="truncate"><span class="font-medium">Doc Hash:</span> {{ certificate.documentHash }}</p>
      <p class="truncate"><span class="font-medium">IPFS CID:</span> {{ certificate.ipfsCid }}</p>
    </div>

    <div class="flex gap-2">
      <router-link
        :to="`/certificate/${certificate.id}`"
        class="flex-1 px-3 py-2 bg-blue-600 text-white rounded text-sm font-medium hover:bg-blue-700 transition text-center"
      >
        View Details
      </router-link>
      <button
        @click="emit('verify')"
        class="flex-1 px-3 py-2 bg-gray-200 text-gray-900 rounded text-sm font-medium hover:bg-gray-300 transition"
      >
        Verify
      </button>
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
