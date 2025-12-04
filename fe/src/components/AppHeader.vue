<template>
  <header class="sticky top-0 z-50 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white shadow-lg border-b border-slate-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <router-link to="/" class="flex items-center gap-3 hover:opacity-80 transition">
          <h1 class="text-2xl font-bold bg-gradient-to-r from-purple-400 to-purple-300 bg-clip-text text-transparent">
            DiplomaChain
          </h1>
        </router-link>

        <nav class="hidden md:flex items-center gap-8">
          <router-link to="/" class="text-gray-300 hover:text-purple-400 transition font-medium" :class="{ 'text-purple-400': $route.path === '/' }">
            Home
          </router-link>
          <router-link to="/explorer" class="text-gray-300 hover:text-purple-400 transition font-medium" :class="{ 'text-purple-400': $route.path === '/explorer' }">
            Explorer
          </router-link>
          <router-link to="/verify" class="text-gray-300 hover:text-purple-400 transition font-medium" :class="{ 'text-purple-400': $route.path === '/verify' }">
            Verify
          </router-link>
        </nav>

        <div class="flex items-center gap-3 sm:gap-4 w-full sm:w-auto">
          <div v-if="authStore.isAuthenticated" class="hidden sm:block text-right">
            <p class="text-xs text-gray-400">{{ authStore.userRole }}</p>
            <p class="text-sm font-mono text-purple-400 truncate">{{ truncateAddress(authStore.userAddress) }}</p>
          </div>
          <!-- <ToggleTheme /> -->
          <button v-if="authStore.isAuthenticated" @click="handleLogout" class="px-4 py-2 bg-red-600/80 hover:bg-red-600 rounded-lg transition text-sm font-medium text-white">
            Logout
          </button>
          <router-link v-if="!authStore.isAuthenticated" to="/login" class="px-4 py-2 bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-600 rounded-lg transition text-sm font-medium text-white whitespace-nowrap">
            Connect Wallet
          </router-link>
        </div>
      </div>

      <nav class="md:hidden flex items-center gap-4 mt-4 pt-4 border-t border-slate-700">
        <router-link to="/explorer" class="text-xs text-gray-300 hover:text-purple-400 transition font-medium">
          Explorer
        </router-link>
        <router-link to="/verify" class="text-xs text-gray-300 hover:text-purple-400 transition font-medium">
          Verify
        </router-link>
      </nav>
    </div>
  </header>
</template>


<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router';
// import ThemeToggle from "@/components/ThemeToggle.vue";
// import { ToggleTheme } from './ToggleTheme.vue';

const authStore = useAuthStore();
const router = useRouter();

const truncateAddress = (address: string | null): string => {
  if (!address) return '';
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
};

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};
</script>
