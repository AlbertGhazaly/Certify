<template>
  <div class="min-h-screen bg-background py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-2xl mx-auto">
      <router-link to="/admin" class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8">
        <span>←</span> Back
      </router-link>

      <div class="bg-card border border-border rounded-xl p-6 sm:p-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-foreground mb-2">Revoke Diploma</h1>
        <p class="text-muted-foreground mb-8">Revoke or invalidate an issued diploma certificate</p>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Certificate Selection -->
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">Select Certificate *</label>
            <select
              v-model="selectedCertificateId"
              required
              class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            >
              <option value="">-- Choose a certificate --</option>
              <option value="cert1">John Smith - STU_12345678 - B.S. Computer Science</option>
              <option value="cert2">Jane Doe - STU_12345679 - B.A. Business</option>
            </select>
          </div>

          <!-- Selected Certificate Details -->
          <template v-if="selectedCertificateId">
            <div class="bg-background rounded-lg p-4 border border-border">
              <h3 class="font-semibold text-foreground mb-3">Certificate Details</h3>
              <div class="space-y-2 text-sm">
                <p><span class="font-medium text-foreground">Student:</span> <span class="text-muted-foreground">John Smith</span></p>
                <p><span class="font-medium text-foreground">ID:</span> <span class="text-muted-foreground">STU_12345678</span></p>
                <p><span class="font-medium text-foreground">Degree:</span> <span class="text-muted-foreground">B.S. Computer Science</span></p>
                <p><span class="font-medium text-foreground">Issued:</span> <span class="text-muted-foreground">December 15, 2023</span></p>
              </div>
            </div>
          </template>

          <!-- Revocation Reason -->
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">Reason for Revocation *</label>
            <select
              v-model="form.reason"
              required
              class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
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
            <label class="block text-sm font-medium text-foreground mb-2">Additional Details</label>
            <textarea
              v-model="form.details"
              rows="4"
              placeholder="Provide details about the revocation..."
              class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            />
          </div>

          <!-- Confirmation -->
          <div class="bg-destructive/10 border border-destructive/50 rounded-lg p-4">
            <label class="flex items-center gap-2">
              <input
                v-model="form.confirmed"
                type="checkbox"
                class="rounded border border-border"
              />
              <span class="text-sm text-destructive">
                I understand that revoking this diploma is permanent and cannot be undone
              </span>
            </label>
          </div>

          <!-- Submit -->
          <div class="flex flex-col sm:flex-row gap-4 pt-4">
            <button
              type="submit"
              :disabled="isSubmitting || !form.confirmed"
              class="flex-1 px-6 py-3 bg-destructive text-white rounded-lg font-medium hover:bg-destructive/90 disabled:bg-muted transition"
            >
              {{ isSubmitting ? 'Processing...' : 'Revoke Diploma' }}
            </button>
            <button
              type="reset"
              class="px-6 py-3 bg-secondary text-foreground rounded-lg font-medium hover:bg-secondary/80 transition"
            >
              Cancel
            </button>
          </div>

          <!-- Messages -->
          <div v-if="successMessage" class="bg-accent/10 border border-accent/50 rounded-lg p-4 text-accent">
            {{ successMessage }}
          </div>
          <div v-if="errorMessage" class="bg-destructive/10 border border-destructive/50 rounded-lg p-4 text-destructive">
            {{ errorMessage }}
          </div>
        </form>
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
