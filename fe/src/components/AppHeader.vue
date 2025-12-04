<template>
  <header class="bg-slate-900 text-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
      <router-link to="/" class="flex items-center gap-2">
        <div class="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center font-bold">
          BD
        </div>
        <h1 class="text-xl font-bold">Diploma Chain</h1>
      </router-link>

      <nav class="hidden md:flex items-center gap-8">
        <router-link
          to="/"
          class="hover:text-blue-400 transition"
          :class="{ 'text-blue-400': $route.path === '/' }"
        >
          Home
        </router-link>
        <router-link
          to="/explorer"
          class="hover:text-blue-400 transition"
          :class="{ 'text-blue-400': $route.path === '/explorer' }"
        >
          Explorer
        </router-link>
        <router-link
          to="/verify"
          class="hover:text-blue-400 transition"
          :class="{ 'text-blue-400': $route.path === '/verify' }"
        >
          Verify
        </router-link>
      </nav>

      <div class="flex items-center gap-4">
        <template v-if="authStore.isAuthenticated">
          <div class="hidden sm:block text-sm">
            <p class="text-gray-400">{{ authStore.userRole }}</p>
            <p class="text-blue-400 truncate">{{ truncateAddress(authStore.userAddress) }}</p>
          </div>
          <button
            @click="handleLogout"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition text-sm font-medium"
          >
            Logout
          </button>
        </template>
        <template v-else>
          <router-link
            to="/login"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition text-sm font-medium"
          >
            Connect Wallet
          </router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router';

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
