<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-white mb-2">Select Your Role</h2>
      <p class="text-gray-400">Choose how you want to interact with the Diploma Chain system</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <button
        v-for="role in roles"
        :key="role.value"
        @click="selectRole(role.value)"
        :class="[
          'group p-6 rounded-xl border-2 transition-all duration-300 text-left overflow-hidden relative',
          selectedRole === role.value
            ? 'border-purple-500 bg-gradient-to-br from-purple-900/20 to-purple-800/10 shadow-lg shadow-purple-500/20'
            : 'border-slate-700 bg-slate-800/50 hover:border-purple-500/50 hover:bg-slate-800/80'
        ]"
      >
        <!-- Background Gradient Effect -->
        <div v-if="selectedRole === role.value" class="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-transparent pointer-events-none" />

        <div class="relative z-10">
          <!-- Icon Container -->
          <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center mb-3 group-hover:shadow-lg group-hover:shadow-purple-500/50 transition">
            <span class="text-white text-lg">{{ role.icon }}</span>
          </div>

          <!-- Role Name -->
          <div class="font-bold text-lg text-white mb-1">{{ role.label }}</div>

          <!-- Description -->
          <div class="text-sm text-gray-400 leading-relaxed">{{ role.description }}</div>

          <!-- Features List -->
          <div v-if="role.features" class="mt-4 pt-4 border-t border-slate-700">
            <ul class="text-xs text-gray-400 space-y-2">
              <li v-for="(feature, idx) in role.features" :key="idx" class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-purple-500" />
                {{ feature }}
              </li>
            </ul>
          </div>

          <!-- Selection Indicator -->
          <div v-if="selectedRole === role.value" class="mt-4 flex items-center gap-2 text-purple-400 text-sm font-medium">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            Selected
          </div>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  modelValue?: string;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: string];
}>();

const roles = [
  {
    value: 'admin',
    label: 'Institution Admin',
    description: 'Issue and revoke diplomas'
  },
  {
    value: 'verifier',
    label: 'Verifier',
    description: 'Verify diploma authenticity'
  },
  {
    value: 'student',
    label: 'Student',
    description: 'View your diplomas'
  },
];

const selectedRole = ref('');

const selectRole = (role: string) => {
  selectedRole.value = role;
  emit('update:modelValue', role);
};
</script>
