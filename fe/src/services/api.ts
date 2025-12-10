import axios from 'axios';
import type { Student, StudentCreate } from '@/types';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Adjust the base URL as needed
  headers: {
    'Content-Type': 'application/json',
  },
});

// Example function to get users
export const getUsers = async () => {
  try {
    const response = await apiClient.get('/users');
    return response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

// Example function to create a user
export const createUser = async (userData) => {
  try {
    const response = await apiClient.post('/users', userData);
    return response.data;
  } catch (error) {
    console.error('Error creating user:', error);
    throw error;
  }
};

// Student API functions
export const getStudents = async (): Promise<Student[]> => {
  try {
    const response = await apiClient.get('/students');
    return response.data;
  } catch (error) {
    console.error('Error fetching students:', error);
    throw error;
  }
};

export const createStudent = async (studentData: StudentCreate): Promise<Student> => {
  try {
    const response = await apiClient.post('/students', studentData);
    return response.data;
  } catch (error) {
    console.error('Error creating student:', error);
    throw error;
  }
};

export const deleteStudent = async (walletAddress: string): Promise<void> => {
  try {
    await apiClient.delete(`/students/${walletAddress}`);
  } catch (error) {
    console.error('Error deleting student:', error);
    throw error;
  }
};

// Add more API functions as needed
