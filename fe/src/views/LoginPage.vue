<!-- eslint-disable vue/no-multiple-template-root -->
<template>
  <div class="min-h-screen bg-background flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-md">
      <!-- Back Button -->
      <router-link
        to="/"
        class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8"
      >
        <span>←</span> Back to Home
      </router-link>

      <div class="bg-card border border-border rounded-xl p-8">
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-foreground mb-2">Connect Wallet</h1>
          <p class="text-muted-foreground">Sign in to your diploma account</p>
        </div>

        <!-- Connect Wallet -->
        <div class="mb-6">
          <button
            @click="handleConnectWallet"
            :disabled="isConnecting"
            class="w-full px-4 py-3 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 disabled:bg-muted disabled:text-muted-foreground transition"
          >
            <span v-if="!isConnecting">Continue with Wallet</span>
            <span v-else>Connecting...</span>
          </button>
        </div>

        <!-- Challenge Sign Step -->
        <template v-if="step === 'sign'">
          <div class="bg-accent/10 border border-accent/50 rounded-lg p-4 mb-6">
            <p class="text-sm text-foreground">
              Please sign the authentication challenge with your wallet to verify ownership
            </p>
          </div>

          <div
            class="mb-6 p-4 bg-background rounded-lg border border-border break-all font-mono text-xs text-muted-foreground"
          >
            {{ authChallenge }}
          </div>

          <button
            @click="handleSignAndLogin"
            :disabled="isSigning"
            class="w-full px-4 py-3 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 disabled:bg-muted disabled:text-muted-foreground transition mb-2"
          >
            <span v-if="!isSigning">Sign Challenge</span>
            <span v-else>Signing...</span>
          </button>

          <button
            @click="step = 'connect'"
            class="w-full px-4 py-3 bg-secondary text-foreground rounded-lg font-semibold hover:bg-secondary/80 transition"
          >
            Back
          </button>
        </template>

        <!-- Error -->
        <div
          v-if="errorMessage"
          class="mt-6 bg-destructive/10 border border-destructive/50 rounded-lg p-4"
        >
          <p class="text-destructive text-sm">{{ errorMessage }}</p>
        </div>

        <p class="text-muted-foreground text-xs text-center mt-6">
          Make sure you're using a supported Web3 wallet like MetaMask
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useWallet } from '@/composables/useWallet'

const router = useRouter()
const authStore = useAuthStore()
const { connectWallet: connectWalletHook, signMessage } = useWallet()

const step = ref<'connect' | 'sign'>('connect')
const authChallenge = ref('')
const isConnecting = ref(false)
const isSigning = ref(false)
const errorMessage = ref('')

const handleConnectWallet = async () => {
  isConnecting.value = true
  errorMessage.value = ''

  try {
    const address = await connectWalletHook()
    const nonce = await authStore.generateChallenge()

    authChallenge.value = `Authenticate to Diploma Chain\nNonce: ${nonce}`
    step.value = 'sign'
  } catch (e) {
    errorMessage.value = e instanceof Error ? e.message : 'Failed to connect wallet'
  } finally {
    isConnecting.value = false
  }
}

const handleSignAndLogin = async () => {
  isSigning.value = true
  errorMessage.value = ''

  try {
    const signature = await signMessage(authChallenge.value)

    await authStore.login(authStore.user?.address || '', signature)

    router.push('/')
  } catch (e) {
    errorMessage.value = e instanceof Error ? e.message : 'Failed to sign challenge'
  } finally {
    isSigning.value = false
  }
}
</script>
