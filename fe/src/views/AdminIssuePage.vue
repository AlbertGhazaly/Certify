<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="max-w-4xl mx-auto px-4">
      <div class="bg-white rounded-lg shadow-md p-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Issue New Diploma</h1>
        <p class="text-gray-600 mb-8">Create and issue a new digital diploma certificate</p>

        <template v-if="!authStore.isAuthenticated">
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
            <p class="text-blue-900">Please connect your wallet to issue diplomas</p>
            <router-link to="/login" class="mt-2 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Connect Wallet
            </router-link>
          </div>
        </template>

        <template v-else-if="authStore.userRole !== 'admin'">
          <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
            <p class="text-red-900">Only institution admins can issue diplomas</p>
          </div>
        </template>

        <template v-else>
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Student Information -->
            <div>
              <h2 class="text-lg font-semibold text-gray-900 mb-4">Student Information</h2>
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Student Name *</label>
                  <input
                    v-model="form.studentName"
                    type="text"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Full name"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Student ID *</label>
                  <input
                    v-model="form.studentId"
                    type="text"
                    required
                    pattern="\d{8}"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="8 digit ID"
                  />
                </div>
              </div>
            </div>

            <!-- Diploma Information -->
            <div>
              <h2 class="text-lg font-semibold text-gray-900 mb-4">Diploma Information</h2>
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Degree *</label>
                  <input
                    v-model="form.degree"
                    type="text"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., Sarjana Teknik"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Issue Date *</label>
                  <input
                    v-model="form.issueDate"
                    type="date"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>

            <!-- Birth Information -->
            <div>
              <h2 class="text-lg font-semibold text-gray-900 mb-4">Birth Information</h2>
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Birth Place *</label>
                  <input
                    v-model="form.birthPlace"
                    type="text"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="City"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Birth Date *</label>
                  <input
                    v-model="form.birthDate"
                    type="date"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>

            <!-- Document Upload -->
            <div>
              <h2 class="text-lg font-semibold text-gray-900 mb-4">Document Upload</h2>
              <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition">
                <input
                  ref="fileInput"
                  type="file"
                  accept=".pdf"
                  @change="handleFileUpload"
                  class="hidden"
                />
                <button
                  type="button"
                  @click="$refs.fileInput?.$el.click()"
                  class="text-blue-600 hover:text-blue-700 font-medium"
                >
                  Click to upload or drag and drop
                </button>
                <p class="text-sm text-gray-500 mt-2">PDF up to 100KB</p>
                <p v-if="form.documentFile" class="mt-2 text-sm text-green-600">
                  ✓ {{ form.documentFile.name }}
                </p>
              </div>
            </div>

            <!-- Encryption Key -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Encryption Key *</label>
              <input
                v-model="form.encryptionKey"
                type="password"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="AES encryption key"
              />
              <p class="text-xs text-gray-600 mt-1">Used to encrypt the diploma PDF</p>
            </div>

            <!-- Submit -->
            <div class="flex gap-4 pt-4">
              <button
                type="submit"
                :disabled="isSubmitting"
                class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 transition"
              >
                <span v-if="!isSubmitting">Issue Diploma</span>
                <span v-else>Processing...</span>
              </button>
              <button
                type="reset"
                class="px-6 py-3 bg-gray-200 text-gray-900 rounded-lg font-medium hover:bg-gray-300 transition"
              >
                Clear
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
