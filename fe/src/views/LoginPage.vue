<!-- eslint-disable vue/no-multiple-template-root -->
<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4">
    <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2 text-center">Connect Wallet</h1>
      <p class="text-gray-600 text-center mb-8">Sign in to your diploma account</p>

      <template v-if="step === 'role'">
        <RoleSelector v-model="selectedRole" class="mb-6" />
        <button
          @click="handleConnectWallet"
          :disabled="!selectedRole || isConnecting"
          class="w-full px-4 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          <span v-if="!isConnecting">Continue with Wallet</span>
          <span v-else>Connecting...</span>
        </button>
      </template>

      <template v-else-if="step === 'sign'">
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <p class="text-sm text-blue-900">
            Please sign the authentication challenge with your wallet to verify ownership
          </p>
        </div>
        <div class="mb-6 p-4 bg-gray-50 rounded-lg break-all font-mono text-xs text-gray-700">
          {{ authChallenge }}
        </div>
        <button
          @click="handleSignAndLogin"
          :disabled="isSigning"
          class="w-full px-4 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          <span v-if="!isSigning">Sign Challenge</span>
          <span v-else>Signing...</span>
        </button>
        <button
          @click="step = 'role'"
          class="w-full mt-2 px-4 py-3 bg-gray-200 text-gray-900 rounded-lg font-semibold hover:bg-gray-300 transition"
        >
          Back
        </button>
      </template>

      <div v-if="errorMessage" class="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
        <p class="text-red-900 text-sm">{{ errorMessage }}</p>
      </div>

      <p class="text-gray-600 text-xs text-center mt-6">
        Make sure you're using a supported Web3 wallet like MetaMask
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useWallet } from '@/composables/useWallet'
import RoleSelector from '@/components/RoleSelector.vue'

const router = useRouter()
const authStore = useAuthStore()
const { connectWallet: connectWalletHook, signMessage } = useWallet()

const step = ref<'role' | 'sign'>('role')
const selectedRole = ref('')
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
    authChallenge.value = `Authenticate to Diploma Chain\nNonce: ${nonce}\nRole: ${selectedRole.value}`
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
    await authStore.login(
      authStore.user?.address || '',
      signature,
      selectedRole.value as 'admin' | 'verifier' | 'student'
    )
    
    if (selectedRole.value === 'admin') {
      router.push('/admin/issue')
    } else if (selectedRole.value === 'verifier') {
      router.push('/verify')
    } else {
      router.push('/')
    }
  } catch (e) {
    errorMessage.value = e instanceof Error ? e.message : 'Failed to sign challenge'
  } finally {
    isSigning.value = false
  }
}
</script>
