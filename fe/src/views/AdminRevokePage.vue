<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="max-w-2xl mx-auto px-4">
      <div class="bg-white rounded-lg shadow-md p-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Revoke Diploma</h1>
        <p class="text-gray-600 mb-8">Revoke or invalidate an issued diploma certificate</p>

        <template v-if="!authStore.isAuthenticated">
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
            <p class="text-blue-900">Please connect your wallet to revoke diplomas</p>
            <router-link to="/login" class="mt-2 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Connect Wallet
            </router-link>
          </div>
        </template>

        <template v-else-if="authStore.userRole !== 'admin'">
          <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
            <p class="text-red-900">Only institution admins can revoke diplomas</p>
          </div>
        </template>

        <template v-else>
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Certificate Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Select Certificate to Revoke *</label>
              <select
                v-model="selectedCertificateId"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">-- Choose a certificate --</option>
                <option
                  v-for="cert in activeCertificates"
                  :key="cert.id"
                  :value="cert.id"
                >
                  {{ cert.studentName }} ({{ cert.studentId }}) - {{ cert.degree }}
                </option>
              </select>
            </div>

            <!-- Selected Certificate Details -->
            <template v-if="selectedCertificate">
              <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h3 class="font-semibold text-gray-900 mb-3">Certificate Details</h3>
                <div class="space-y-2 text-sm">
                  <p><span class="font-medium">Student:</span> {{ selectedCertificate.studentName }}</p>
                  <p><span class="font-medium">ID:</span> {{ selectedCertificate.studentId }}</p>
                  <p><span class="font-medium">Degree:</span> {{ selectedCertificate.degree }}</p>
                  <p><span class="font-medium">Issued:</span> {{ formatDate(selectedCertificate.issueDate) }}</p>
                </div>
              </div>
            </template>

            <!-- Revocation Reason -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Reason for Revocation *</label>
              <select
                v-model="form.reason"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">-- Select reason --</option>
                <option value="fraud">Fraud Detected</option>
                <option value="invalid">Invalid Credentials</option>
                <option value="graduation-cancelled">Graduation Cancelled</option>
                <option value="other">Other</option>
              </select>
            </div>

            <!-- Additional Details -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Additional Details</label>
              <textarea
                v-model="form.details"
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Provide additional details about the revocation..."
              />
            </div>

            <!-- Confirmation -->
            <div class="bg-red-50 border border-red-200 rounded-lg p-4">
              <label class="flex items-center gap-2">
                <input
                  v-model="form.confirmed"
                  type="checkbox"
                  class="rounded border-gray-300"
                />
                <span class="text-sm text-red-900">
                  I understand that revoking this diploma is permanent and cannot be undone
                </span>
              </label>
            </div>

            <!-- Submit -->
            <div class="flex gap-4 pt-4">
              <button
                type="submit"
                :disabled="isSubmitting || !form.confirmed"
                class="flex-1 px-6 py-3 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 disabled:bg-gray-400 transition"
              >
                <span v-if="!isSubmitting">Revoke Diploma</span>
                <span v-else>Processing...</span>
              </button>
              <button
                type="reset"
                class="px-6 py-3 bg-gray-200 text-gray-900 rounded-lg font-medium hover:bg-gray-300 transition"
              >
                Cancel
              </button>
            </div>

            <!-- Messages -->
            <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-lg p-4 text-green-900">
              {{ successMessage }}
            </div>
            <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-900">
              {{ errorMessage }}
            </div>
          </form>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useCertificateStore } from '@/stores/certificateStore';
import { useBlockchain } from '@/composables/useBlockchain';
import { CryptoUtils } from '@/utils/crypto';

const authStore = useAuthStore();
const certificateStore = useCertificateStore();
const { revokeCertificate, isLoading: isSubmitting } = useBlockchain();

const form = ref({
  reason: '',
  details: '',
  confirmed: false,
});

const selectedCertificateId = ref('');
const successMessage = ref('');
const errorMessage = ref('');

const activeCertificates = computed(() => certificateStore.activeCertificates);
const selectedCertificate = computed(() =>
  certificateStore.getCertificateById(selectedCertificateId.value)
);

const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const handleSubmit = async () => {
  if (!selectedCertificateId.value || !authStore.userAddress || !form.value.reason) {
    errorMessage.value = 'Please fill in all required fields';
    return;
  }

  errorMessage.value = '';
  successMessage.value = '';

  try {
    const signature = await CryptoUtils.sign(
      `revoke_${selectedCertificateId.value}_${form.value.reason}`,
      authStore.userAddress
    );

    const transaction = await revokeCertificate(
      selectedCertificateId.value,
      form.value.reason,
      authStore.userAddress,
      signature.signature
    );

    certificateStore.updateCertificate(selectedCertificateId.value, { status: 'revoked' });
    certificateStore.addTransaction(transaction);

    successMessage.value = 'Diploma revoked successfully!';
    form.value = { reason: '', details: '', confirmed: false };
    selectedCertificateId.value = '';
  } catch (e) {
    errorMessage.value = e instanceof Error ? e.message : 'Failed to revoke diploma';
  }
};
</script>
