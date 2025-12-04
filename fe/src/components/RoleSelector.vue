<template>
  <div class="space-y-4">
    <h2 class="text-lg font-semibold">Select Your Role</h2>
    <div class="grid md:grid-cols-3 gap-4">
      <button
        v-for="role in roles"
        :key="role.value"
        @click="selectRole(role.value)"
        :class="[
          'p-4 rounded-lg border-2 transition text-left',
          selectedRole === role.value
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-200 hover:border-blue-300'
        ]"
      >
        <div class="font-semibold text-gray-900">{{ role.label }}</div>
        <div class="text-sm text-gray-600 mt-1">{{ role.description }}</div>
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
