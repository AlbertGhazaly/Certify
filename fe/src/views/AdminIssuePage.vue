<template>
  <div class="min-h-screen bg-background py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <router-link to="/" class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8">
        <span>←</span> Back
      </router-link>

      <div class="bg-card border border-border rounded-xl p-6 sm:p-8">
        <h1 class="text-3xl sm:text-4xl font-bold text-foreground mb-2">Issue New Diploma</h1>
        <p class="text-muted-foreground mb-8">Create and issue a new digital diploma certificate</p>

        <form @submit.prevent="handleSubmit" class="space-y-8">
          <!-- Student Information -->
          <div>
            <h2 class="text-lg font-semibold text-foreground mb-4">Student Information</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Student Name *</label>
                <input
                  v-model="form.studentName"
                  type="text"
                  required
                  placeholder="Full name"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Student ID *</label>
                <input
                  v-model="form.studentId"
                  type="text"
                  required
                  pattern="\d{8}"
                  placeholder="8 digit ID"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
            </div>
          </div>

          <!-- Diploma Information -->
          <div>
            <h2 class="text-lg font-semibold text-foreground mb-4">Diploma Information</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Degree *</label>
                <input
                  v-model="form.degree"
                  type="text"
                  required
                  placeholder="e.g., B.S. Computer Science"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Issue Date *</label>
                <input
                  v-model="form.issueDate"
                  type="date"
                  required
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
            </div>
          </div>

          <!-- Birth Information -->
          <div>
            <h2 class="text-lg font-semibold text-foreground mb-4">Birth Information</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Birth Place *</label>
                <input
                  v-model="form.birthPlace"
                  type="text"
                  required
                  placeholder="City"
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">Birth Date *</label>
                <input
                  v-model="form.birthDate"
                  type="date"
                  required
                  class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>
            </div>
          </div>

          <!-- Document Upload -->
          <div>
            <h2 class="text-lg font-semibold text-foreground mb-4">Document Upload</h2>
            <div class="border-2 border-dashed border-border rounded-lg p-6 text-center hover:border-accent/50 transition bg-background">
              <p class="text-accent font-medium">Click to upload or drag and drop</p>
              <p class="text-sm text-muted-foreground mt-1">PDF up to 100KB</p>
              <p v-if="form.documentFile" class="mt-2 text-sm text-accent">✓ {{ form.documentFile.name }}</p>
            </div>
          </div>

          <!-- Encryption Key -->
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">Encryption Key *</label>
            <input
              v-model="form.encryptionKey"
              type="password"
              required
              placeholder="AES encryption key"
              class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            />
            <p class="text-xs text-muted-foreground mt-1">Used to encrypt the diploma PDF</p>
          </div>

          <!-- Submit -->
          <div class="flex flex-col sm:flex-row gap-4 pt-4">
            <button
              type="submit"
              :disabled="isSubmitting"
              class="flex-1 px-6 py-3 bg-accent text-accent-foreground rounded-lg font-medium hover:bg-accent/90 disabled:bg-muted transition"
            >
              {{ isSubmitting ? 'Processing...' : 'Issue Diploma' }}
            </button>
            <button
              type="reset"
              class="px-6 py-3 bg-secondary text-foreground rounded-lg font-medium hover:bg-secondary/80 transition"
            >
              Clear
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
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useCertificateStore } from '@/stores/certificateStore';
import { useBlockchain } from '@/composables/useBlockchain';
import { CryptoUtils } from '@/utils/crypto';
import type { IssueCertificatePayload } from '@/types';

const authStore = useAuthStore();
const certificateStore = useCertificateStore();
const { issueCertificate, error: blockchainError } = useBlockchain();

const form = ref({
  studentName: '',
  studentId: '',
  degree: '',
  issueDate: '',
  birthPlace: '',
  birthDate: '',
  documentFile: null as File | null,
  encryptionKey: '',
});

const isSubmitting = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const fileInput = ref();

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file && file.type === 'application/pdf' && file.size <= 100000) {
    form.value.documentFile = file;
  } else {
    errorMessage.value = 'Please select a valid PDF file (max 100KB)';
  }
};

const handleSubmit = async () => {
  if (!authStore.userAddress || !form.value.documentFile) {
    errorMessage.value = 'Missing required information';
    return;
  }

  isSubmitting.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    // Simulate document hashing and IPFS upload
    const documentHash = await CryptoUtils.sha256(form.value.documentFile.name + Date.now());
    const mockIpfsCid = `Qm${Math.random().toString(36).substring(2, 46)}`;
    
    // Create payload
    const payload: IssueCertificatePayload = {
      studentName: form.value.studentName,
      studentId: form.value.studentId,
      degree: form.value.degree,
      birthPlace: form.value.birthPlace,
      birthDate: form.value.birthDate,
      documentHash,
      ipfsCid: mockIpfsCid,
      encryptionKey: form.value.encryptionKey,
    };

    // Sign the certificate
    const signature = await CryptoUtils.sign(JSON.stringify(payload), authStore.userAddress);

    // Issue on blockchain
    const certificate = await issueCertificate(
      payload,
      authStore.userAddress,
      signature.signature
    );

    certificateStore.addCertificate(certificate);
    successMessage.value = `Diploma issued successfully! Certificate ID: ${certificate.id}`;
    
    // Reset form
    form.value = {
      studentName: '',
      studentId: '',
      degree: '',
      issueDate: '',
      birthPlace: '',
      birthDate: '',
      documentFile: null,
      encryptionKey: '',
    };
  } catch (e) {
    errorMessage.value = e instanceof Error ? e.message : 'Failed to issue diploma';
  } finally {
    isSubmitting.value = false;
  }
};
</script>
