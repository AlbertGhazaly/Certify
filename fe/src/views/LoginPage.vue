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
          <p class="text-muted-foreground">Sign in with your Ethereum wallet</p>
        </div>

        <!-- Connect Wallet Step -->
        <template v-if="step === 'connect'">
          <div class="mb-6">
            <button
              @click="handleConnectWallet"
              :disabled="isConnecting"
              class="w-full px-4 py-3 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 disabled:bg-muted disabled:text-muted-foreground transition"
            >
              <span v-if="!isConnecting">Connect MetaMask</span>
              <span v-else>Connecting...</span>
            </button>
          </div>
        </template>

        <!-- Challenge Sign Step -->
        <template v-if="step === 'sign'">
          <div class="bg-accent/10 border border-accent/50 rounded-lg p-4 mb-6">
            <p class="text-sm text-foreground font-semibold mb-2">Wallet Connected</p>
            <p class="text-xs text-muted-foreground break-all">{{ connectedAddress }}</p>
          </div>

          <div class="bg-accent/10 border border-accent/50 rounded-lg p-4 mb-6">
            <p class="text-sm text-foreground mb-2">
              Please sign the authentication challenge to verify ownership
            </p>
            <p class="text-xs text-muted-foreground">
              This signature proves you control this wallet without exposing your private key
            </p>
          </div>

          <div
            class="mb-6 p-4 bg-background rounded-lg border border-border break-all font-mono text-xs text-muted-foreground max-h-32 overflow-y-auto"
          >
            {{ authChallenge }}
          </div>

          <button
            @click="handleSignAndLogin"
            :disabled="isSigning"
            class="w-full px-4 py-3 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 disabled:bg-muted disabled:text-muted-foreground transition mb-2"
          >
            <span v-if="!isSigning">Sign & Authenticate</span>
            <span v-else>Signing...</span>
          </button>

          <button
            @click="resetFlow"
            class="w-full px-4 py-3 bg-secondary text-foreground rounded-lg font-semibold hover:bg-secondary/80 transition"
          >
            Cancel
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
          Make sure you have MetaMask installed and connected to Sepolia testnet
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
const { connectWallet: connectWalletHook, signMessage, disconnectWallet } = useWallet()

const step = ref<'connect' | 'sign'>('connect')
const authChallenge = ref('')
const connectedAddress = ref('')
const isConnecting = ref(false)
const isSigning = ref(false)
const errorMessage = ref('')

const handleConnectWallet = async () => {
  isConnecting.value = true
  errorMessage.value = ''

  try {
    // Connect to MetaMask
    const address = await connectWalletHook()
    connectedAddress.value = address
    console.log('Connected address:', address)
    // Request authentication challenge from backend
    const { challenge } = await authStore.requestChallenge(address)
    
    authChallenge.value = challenge
    step.value = 'sign'
    
  } catch (e) {
    errorMessage.value = e instanceof Error ? e.message : 'Failed to connect wallet'
    resetFlow()
  } finally {
    isConnecting.value = false
  }
}

const handleSignAndLogin = async () => {
  isSigning.value = true
  errorMessage.value = ''

  try {
    // Sign the challenge with MetaMask
    const signature = await signMessage(authChallenge.value)

    // Verify signature on backend
    const success = await authStore.verifySignature(connectedAddress.value, signature)

    if (success) {
      router.push('/')
    } else {
      throw new Error('Authentication failed')
    }
  } catch (e) {
    errorMessage.value = e instanceof Error ? e.message : 'Failed to authenticate'
  } finally {
    isSigning.value = false
  }
}

const resetFlow = () => {
  step.value = 'connect'
  authChallenge.value = ''
  connectedAddress.value = ''
  disconnectWallet()
}
</script>