<template>
  <div class="min-h-screen bg-background py-8 px-4">
    <div class="max-w-3xl mx-auto">

      <h1 class="text-3xl font-bold mb-2">Verify Diploma</h1>
      <p class="text-muted-foreground mb-6">
        Enter Student ID (NIM) to verify diploma authenticity
      </p>

      <form
        v-if="!isPublicVerify"
        @submit.prevent="handleVerify"
        class="space-y-4"
      >
        <h1 class="text-3xl font-bold mb-2">
          {{ isPublicVerify ? "Ijazah Terverifikasi" : "Verify Diploma" }}
        </h1>
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
        <div v-if="result.valid &&result.file_url" class="mt-4">
          <p class="text-sm font-semibold">Certificate URL:</p>

          <div class="mt-4 space-y-3">
            <div class="rounded-lg border bg-muted/50 p-4">
              <p class="text-sm font-semibold mb-1">Public Verification Link</p>

              <a
                :href="result.file_url"
                target="_blank"
                class="block text-blue-500 hover:text-blue-400 underline
                      break-all overflow-wrap-anywhere
                      text-sm font-mono"
              >
                {{ result.file_url }}
              </a>
            </div>

            <a
              :href="result.file_url"
              target="_blank"
              download
              class="inline-flex items-center justify-center gap-2
                    px-5 py-2.5
                    bg-green-600 hover:bg-green-700
                    text-white font-semibold
                    rounded-lg
                    transition-colors"
            >
              Download Encrypted Certificate
            </a>
          </div>
        </div>
        <pre
          v-if="result.certificate_text"
          class="bg-muted p-4 rounded text-sm whitespace-pre-wrap break-all overflow-wrap-anywhere hyphens-auto"
        >
{{ result.certificate_text }}
        </pre>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, computed, watch } from "vue"
  import { useRoute } from "vue-router"
  import { verifyCertificateByNIM, verifyPublic } from "@/services/api"
  
  const route = useRoute()
  
  const cid = route.query.cid as string | undefined
  const aesKey = route.query.key as string | undefined
  const certHash = route.query.hash as string | undefined
  
  const isPublicVerify = computed(() => {
    return !!(cid && aesKey && certHash)
  })
  
  const studentId = ref("")
  const loading = ref(false)
  const error = ref("")
  const result = ref<any>(null)
  
  const handleVerify = async () => {
    loading.value = true
    error.value = ""
    result.value = null
  
    try {
      const data = await verifyCertificateByNIM(studentId.value)
      result.value = data
  
      if (!data.success) {
        error.value = data.message
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Verification failed"
    } finally {
      loading.value = false
    }
  }

  const handlePublicVerify = async () => {
    loading.value = true
    error.value = ""
    result.value = null
  
    try {
      const data = await verifyPublic({
        ipfs_cid: cid!,
        aes_key: aesKey!,
        cert_hash: certHash!,
      })
  
      result.value = data
  
      if (!data.success) {
        error.value = data.message
        return
      }
  
      autoDownloadIjazah(data.certificate_text)
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Public verification failed"
    } finally {
      loading.value = false
    }
  }
  

  const autoDownloadIjazah = (text: string) => {
    const blob = new Blob([text], { type: "text/plain;charset=utf-8" })
    const url = URL.createObjectURL(blob)
  
    const a = document.createElement("a")
    a.href = url
    a.download = "ijazah.txt"
    document.body.appendChild(a)
    a.click()
  
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }
  
  onMounted(() => {
    if (isPublicVerify.value) {
      handlePublicVerify()
    }
  })
  </script>
  