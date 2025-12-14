<template>
  <div class="min-h-screen bg-background py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <router-link to="/admin" class="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition mb-8">
        <span>←</span> Back
      </router-link>

      <div class="bg-card border border-border rounded-xl p-6 sm:p-8">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h1 class="text-3xl sm:text-4xl font-bold text-foreground mb-2">Student Management</h1>
            <p class="text-muted-foreground">Manage student records and wallet addresses</p>
          </div>
          <button
            @click="openAddModal"
            class="px-6 py-3 bg-accent text-accent-foreground rounded-lg font-medium hover:bg-accent/90 transition"
          >
            Add Student
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-12">
          <p class="text-muted-foreground">Loading students...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="errorMessage" class="bg-destructive/10 border border-destructive/50 rounded-lg p-4 text-destructive mb-6">
          {{ errorMessage }}
        </div>

        <!-- Students Table -->
        <div v-else-if="students.length > 0" class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-border">
                <th class="text-left py-4 px-4 text-sm font-semibold text-foreground">NIM</th>
                <th class="text-left py-4 px-4 text-sm font-semibold text-foreground">Nama</th>
                <th class="text-left py-4 px-4 text-sm font-semibold text-foreground">Wallet Address</th>
                <th class="text-left py-4 px-4 text-sm font-semibold text-foreground">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="student in students"
                :key="student.wallet_address"
                class="border-b border-border hover:bg-accent/5 transition"
              >
                <td class="py-4 px-4 text-foreground">{{ student.nim }}</td>
                <td class="py-4 px-4 text-foreground">{{ student.nama }}</td>
                <td class="py-4 px-4 text-foreground font-mono text-sm">{{ student.wallet_address }}</td>
                <td class="py-4 px-4">
                  <button
                    @click="confirmDelete(student)"
                    class="px-4 py-2 bg-destructive text-destructive-foreground rounded-lg font-medium hover:bg-destructive/90 transition text-sm"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <p class="text-muted-foreground">No students found. Click "Add Student" to create one.</p>
        </div>
      </div>
    </div>

    <!-- Add Student Modal -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
      @click.self="closeAddModal"
    >
      <div class="bg-card border border-border rounded-xl p-6 sm:p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold text-foreground mb-6">Add New Student</h2>

        <form @submit.prevent="handleAddStudent" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">NIM *</label>
            <input
              v-model="newStudent.nim"
              type="text"
              required
              placeholder="Student ID Number"
              class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-foreground mb-2">Nama *</label>
            <input
              v-model="newStudent.nama"
              type="text"
              required
              placeholder="Full Name"
              class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-foreground mb-2">Wallet Address *</label>
            <input
              v-model="newStudent.wallet_address"
              type="text"
              required
              placeholder="0x..."
              class="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            />
          </div>

          <div v-if="modalError" class="bg-destructive/10 border border-destructive/50 rounded-lg p-3 text-destructive text-sm">
            {{ modalError }}
          </div>

          <div class="flex gap-3 pt-4">
            <button
              type="submit"
              :disabled="isSubmitting"
              class="flex-1 px-6 py-3 bg-accent text-accent-foreground rounded-lg font-medium hover:bg-accent/90 disabled:bg-muted transition"
            >
              {{ isSubmitting ? 'Adding...' : 'Submit' }}
            </button>
            <button
              type="button"
              @click="closeAddModal"
              :disabled="isSubmitting"
              class="px-6 py-3 bg-secondary text-foreground rounded-lg font-medium hover:bg-secondary/80 disabled:bg-muted transition"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
      @click.self="closeDeleteModal"
    >
      <div class="bg-card border border-border rounded-xl p-6 sm:p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold text-foreground mb-4">Confirm Delete</h2>
        <p class="text-muted-foreground mb-6">
          Are you sure you want to delete student <strong class="text-foreground">{{ studentToDelete?.nama }}</strong> ({{ studentToDelete?.nim }})?
          This action cannot be undone.
        </p>

        <div class="flex gap-3">
          <button
            @click="handleDeleteStudent"
            :disabled="isDeleting"
            class="flex-1 px-6 py-3 bg-destructive text-destructive-foreground rounded-lg font-medium hover:bg-destructive/90 disabled:bg-muted transition"
          >
            {{ isDeleting ? 'Deleting...' : 'Delete' }}
          </button>
          <button
            @click="closeDeleteModal"
            :disabled="isDeleting"
            class="px-6 py-3 bg-secondary text-foreground rounded-lg font-medium hover:bg-secondary/80 disabled:bg-muted transition"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getStudents, createStudent, deleteStudent } from '@/services/api';
import type { Student, StudentCreate } from '@/types';

const students = ref<Student[]>([]);
const isLoading = ref(false);
const errorMessage = ref('');

const showAddModal = ref(false);
const newStudent = ref<StudentCreate>({
  nim: '',
  nama: '',
  wallet_address: '',
});
const isSubmitting = ref(false);
const modalError = ref('');

const showDeleteModal = ref(false);
const studentToDelete = ref<Student | null>(null);
const isDeleting = ref(false);

// Fetch students on component mount
onMounted(() => {
  fetchStudents();
});

const fetchStudents = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    students.value = await getStudents();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to load students';
  } finally {
    isLoading.value = false;
  }
};

const openAddModal = () => {
  showAddModal.value = true;
  modalError.value = '';
  newStudent.value = {
    nim: '',
    nama: '',
    wallet_address: '',
  };
};

const closeAddModal = () => {
  showAddModal.value = false;
  modalError.value = '';
};

const handleAddStudent = async () => {
  isSubmitting.value = true;
  modalError.value = '';

  try {
    await createStudent(newStudent.value);
    closeAddModal();
    await fetchStudents(); // Refresh the table
  } catch (error) {
    modalError.value = error instanceof Error ? error.message : 'Failed to add student';
  } finally {
    isSubmitting.value = false;
  }
};

const confirmDelete = (student: Student) => {
  studentToDelete.value = student;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  studentToDelete.value = null;
};

const handleDeleteStudent = async () => {
  if (!studentToDelete.value) return;

  isDeleting.value = true;
  try {
    await deleteStudent(studentToDelete.value.wallet_address);
    closeDeleteModal();
    await fetchStudents(); // Refresh the table
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to delete student';
    closeDeleteModal();
  } finally {
    isDeleting.value = false;
  }
};
</script>
