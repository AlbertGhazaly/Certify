<template>
  <div class="min-h-screen bg-background py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <router-link to="/explorer" class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8">
        <span>←</span> Back to Explorer
      </router-link>

      <div class="bg-card border border-border rounded-xl p-6 sm:p-8 mb-8">
        <div class="mb-6 pb-6 border-b border-border">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4">
            <div>
              <h1 class="text-3xl font-bold text-foreground">John Smith</h1>
              <p class="text-muted-foreground mt-1">Student ID: STU_12345678</p>
            </div>
            <span class="px-4 py-2 bg-accent/20 text-accent rounded-full text-sm font-semibold">ACTIVE</span>
          </div>
        </div>

        <div class="bg-gradient-to-br from-accent/10 via-primary/10 to-accent/10 rounded-lg p-6 sm:p-8 mb-8 border border-accent/30">
          <div class="text-center space-y-4">
            <p class="text-muted-foreground">Kementerian Pendidikan Tinggi, Sains, dan Teknologi</p>
            <p class="text-foreground">University of Technology</p>
            <p class="text-muted-foreground mt-6">Hereby certifies that</p>
            <p class="text-2xl font-bold text-foreground mt-4">John Smith</p>
            <p class="text-muted-foreground">Has successfully completed all requirements for</p>
            <p class="text-lg font-semibold text-accent mt-4">Bachelor of Science in Computer Science</p>
            <p class="text-muted-foreground mt-6">Awarded at University of Technology</p>
            <p class="text-muted-foreground">December 15, 2023</p>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
          <div class="bg-background rounded-lg p-4 border border-border">
            <h3 class="font-semibold text-foreground mb-2">Issued By</h3>
            <p class="font-mono text-sm text-muted-foreground break-all">0x1234567890abcdef...</p>
          </div>
          <div class="bg-background rounded-lg p-4 border border-border">
            <h3 class="font-semibold text-foreground mb-2">Issue Date</h3>
            <p class="text-muted-foreground">December 15, 2023</p>
          </div>
        </div>

        <div class="space-y-4 mb-8">
          <div class="bg-background rounded-lg p-4 border border-border">
            <h3 class="font-semibold text-foreground mb-2">Document Hash (SHA-256)</h3>
            <p class="font-mono text-xs text-muted-foreground break-all bg-card p-2 rounded">
              0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
            </p>
          </div>
          <div class="bg-background rounded-lg p-4 border border-border">
            <h3 class="font-semibold text-foreground mb-2">IPFS CID</h3>
            <p class="font-mono text-xs text-muted-foreground break-all bg-card p-2 rounded">
              QmX1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z
            </p>
          </div>
          <div class="bg-background rounded-lg p-4 border border-border">
            <h3 class="font-semibold text-foreground mb-2">Signature Hash</h3>
            <p class="font-mono text-xs text-muted-foreground break-all bg-card p-2 rounded">
              0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
            </p>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row gap-4 pt-4 border-t border-border">
          <button class="flex-1 px-4 py-2 bg-accent text-accent-foreground rounded-lg font-medium hover:bg-accent/90 transition">
            Download Certificate
          </button>
          <button class="flex-1 px-4 py-2 bg-secondary text-foreground rounded-lg font-medium hover:bg-secondary/80 transition">
            Verify on Blockchain
          </button>
          <router-link to="/explorer" class="flex-1 px-4 py-2 bg-card border border-border text-foreground rounded-lg font-medium hover:bg-secondary transition text-center">
            View on Explorer
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCertificateStore } from '@/stores/certificateStore'
import type { Certificate } from '@/types'

const route = useRoute()
const certificateStore = useCertificateStore()

const certificate = ref<Certificate | null>(null)
const isLoading = ref(true)

const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const downloadCertificate = () => {
  alert('Certificate download feature would be implemented with actual PDF generation')
}

const verifyCertificate = () => {
  alert('Certificate verification initiated')
}

onMounted(() => {
  const certificateId = route.params.id as string
  certificate.value = certificateStore.getCertificateById(certificateId)
  
  isLoading.value = false
})
</script>
