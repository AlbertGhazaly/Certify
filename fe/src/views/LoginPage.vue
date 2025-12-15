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
          <h1 class="text-3xl font-bold text-foreground mb-2">Issuer Login</h1>
          <p class="text-muted-foreground">Connect your wallet to authenticate as an issuer</p>
        </div>

        <!-- Connect Wallet Step -->
        <template v-if="step === 'connect'">
          <div class="mb-6">
            <button
              @click="handleConnectWallet"
              :disabled="isConnecting"
              class="w-full px-4 py-3 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 disabled:bg-muted disabled:text-muted-foreground transition"
            >
              <span v-if="!isConnecting">🦊 Connect MetaMask</span>
              <span v-else>⏳ Connecting...</span>
            </button>
          </div>
        </template>

        <!-- Challenge Sign Step -->
        <template v-if="step === 'sign'">
          <div class="bg-accent/10 border border-accent/50 rounded-lg p-4 mb-6">
            <p class="text-sm text-foreground font-semibold mb-2">✅ Wallet Connected</p>
            <p class="text-xs text-muted-foreground break-all">{{ connectedAddress }}</p>
          </div>

          <div class="bg-accent/10 border border-accent/50 rounded-lg p-4 mb-6">
            <p class="text-sm text-foreground mb-2">
              🔐 Sign the authentication challenge
            </p>
            <p class="text-xs text-muted-foreground">
              This signature proves you control this wallet and validates your issuer status on the Sepolia blockchain.
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
            <span v-if="!isSigning">✍️ Sign & Authenticate</span>
            <span v-else>⏳ Verifying...</span>
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
          <p class="text-destructive text-sm font-semibold mb-1">❌ Authentication Failed</p>
          <p class="text-destructive text-sm">{{ errorMessage }}</p>
        </div>

        <!-- Info Box -->
        <div class="mt-6 bg-muted/50 border border-border rounded-lg p-4">
          <p class="text-xs text-muted-foreground mb-2">
            <strong>Requirements:</strong>
          </p>
          <ul class="text-xs text-muted-foreground space-y-1">
            <li>• MetaMask browser extension installed</li>
            <li>• Connected to Sepolia testnet</li>
            <li>• Wallet registered as an issuer on the smart contract</li>
          </ul>
        </div>
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
    // Check if MetaMask is installed
    if (!window.ethereum) {
      throw new Error('MetaMask is not installed. Please install MetaMask to continue.')
    }

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

    // Verify signature and validate issuer status on backend
    const success = await authStore.verifySignature(connectedAddress.value, signature)

    if (success) {
      // Redirect to admin page (user is now authenticated as issuer)
      router.push('/admin')
    } else {
      throw new Error('Authentication failed. Please try again.')
    }
  } catch (e: any) {
    // Handle specific error messages
    if (e.message.includes('Only issuers') || e.message.includes('Access denied')) {
      errorMessage.value = 'Access Denied: Your wallet is not registered as an issuer on the Sepolia blockchain.'
    } else if (e.message.includes('signature')) {
      errorMessage.value = 'Invalid signature. Please try signing again.'
    } else if (e.message.includes('expired')) {
      errorMessage.value = 'Challenge expired. Please reconnect and try again.'
      resetFlow()
    } else {
      errorMessage.value = e instanceof Error ? e.message : 'Failed to authenticate'
    }
  } finally {
    isSigning.value = false
  }
}

const resetFlow = () => {
  step.value = 'connect'
  authChallenge.value = ''
  connectedAddress.value = ''
  errorMessage.value = ''
  disconnectWallet()
}
</script>

<style scoped>
/* Add any additional custom styles if needed */
</style>