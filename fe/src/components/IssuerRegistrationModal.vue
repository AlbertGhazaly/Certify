<script setup lang="ts">
  import { ref, computed, watch } from "vue"
  import { useAuthStore } from "@/stores/authStore"
  import { createIssuerRegistration } from "@/services/api"
  
  const emit = defineEmits(["close"])
  const authStore = useAuthStore()
  
  const name = ref("")
  const walletAddress = ref("")
  const loading = ref(false)
  const success = ref(false)
  const error = ref<string | null>(null)
  
  watch(
    () => authStore.userAddress,
    (addr) => {
      if (addr) walletAddress.value = addr
    },
    { immediate: true }
  )
  
  const isFormValid = computed(() =>
    name.value.trim() !== "" && walletAddress.value !== ""
  )
  
  const submit = async () => {
    if (!isFormValid.value) return
    loading.value = true
    error.value = null
  
    try {
      await createIssuerRegistration({
        name: name.value,
        wallet_address: walletAddress.value,
      })
      success.value = true
    } catch (e: any) {
      error.value = e?.response?.data?.detail || "Registration failed"
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <template>
    <teleport to="body">
      <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-background p-6 rounded-xl w-full max-w-md">
          <h3 class="text-xl font-semibold mb-4">Issuer Registration</h3>
  
          <p v-if="success" class="text-green-600 mb-4">
            Registration successful!
          </p>
  
          <p v-if="error" class="text-red-500 mb-4">
            {{ error }}
          </p>
  
          <input
            v-model="name"
            placeholder="Institution name"
            class="w-full mb-3 px-3 py-2 border rounded-lg"
          />
  
          <input
            v-model="walletAddress"
            disabled
            class="w-full mb-4 px-3 py-2 border rounded-lg bg-muted"
          />
  
          <div class="flex justify-end gap-2">
            <button @click="emit('close')" class="px-4 py-2 border rounded-lg">
              Cancel
            </button>
            <button
              @click="submit"
              :disabled="!isFormValid || loading"
              class="px-4 py-2 rounded-lg bg-accent text-accent-foreground disabled:opacity-50"
            >
              {{ loading ? "Submitting..." : "Register" }}
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </template>