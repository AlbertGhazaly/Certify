<template>
  <button
    @click="toggleTheme"
    class="p-2 rounded-xl transition border bg-card text-card-foreground hover:bg-muted"
  >
    <span v-if="isDark">🌙</span>
    <span v-else>☀️</span>
  </button>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

const isDark = ref(false);

function applyTheme(dark: boolean) {
  const root = document.documentElement;

  if (dark) root.classList.add("dark");
  else root.classList.remove("dark");

  localStorage.setItem("theme", dark ? "dark" : "light");
}

function toggleTheme() {
  isDark.value = !isDark.value;
  applyTheme(isDark.value);
}

onMounted(() => {
  // 1. Load from localStorage if exists
  const saved = localStorage.getItem("theme");

  if (saved === "dark") isDark.value = true;
  else if (saved === "light") isDark.value = false;
  else {
    // 2. Otherwise follow system preference
    isDark.value = window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  applyTheme(isDark.value);
});
</script>
