<template>
  <div class="min-h-screen bg-background py-8 px-4">
    <div class="max-w-3xl mx-auto">

      <h1 class="text-3xl font-bold mb-2">Verify Diploma</h1>
      <p class="text-muted-foreground mb-6">
        Enter Student ID (NIM) to verify diploma authenticity
      </p>

      <form @submit.prevent="handleVerify" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">
            Student ID (NIM)
          </label>
          <input
            v-model="studentId"
            required
            placeholder="11223029"
            class="w-full px-4 py-2 border rounded-lg"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2 bg-accent text-accent-foreground rounded-lg"
        >
          {{ loading ? 'Verifying...' : 'Verify Certificate' }}
        </button>
      </form>

      <!-- Error -->
      <div
        v-if="error"
        class="mt-6 p-4 bg-destructive/10 border border-destructive text-destructive rounded-lg"
      >
        {{ error }}
      </div>

      <!-- Result -->
      <div
        v-if="result"
        class="mt-6 p-6 rounded-lg border"
        :class="result.valid ? 'border-accent' : 'border-destructive'"
      >
        <h2 class="text-xl font-bold mb-2">
          {{ result.valid ? 'Certificate Valid' : 'Certificate Invalid' }}
        </h2>

        <p class="mb-4">{{ result.message }}</p>

        <pre
          v-if="result.certificate_text"
          class="bg-muted p-4 rounded text-sm whitespace-pre-wrap"
        >
{{ result.certificate_text }}
        </pre>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { verifyCertificateByNIM } from '@/services/api'
  
  const studentId = ref('')
  const loading = ref(false)
  const error = ref('')
  const result = ref<any>(null)
  
  const handleVerify = async () => {
    loading.value = true
    error.value = ''
    result.value = null
  
    try {
      const data = await verifyCertificateByNIM(studentId.value)
  
      result.value = data
      if (!data.success) {
        error.value = data.message
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Verification failed'
    } finally {
      loading.value = false
    }
  }
  </script>
  