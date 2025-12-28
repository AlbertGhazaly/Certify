import axios from 'axios';
import type { Student, StudentCreate } from '@/types';
import type {
  IssuerRegistration,
  IssuerRegistrationCreate,
  IssuerRegistrationListResponse,
  IssuerRegistrationListParams,
} from '@/types';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getUsers = async () => {
  try {
    const response = await apiClient.get('/users');
    return response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

export const createUser = async (userData) => {
  try {
    const response = await apiClient.post('/users', userData);
    return response.data;
  } catch (error) {
    console.error('Error creating user:', error);
    throw error;
  }
};

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


export const createIssuerRegistration = async (
  data: IssuerRegistrationCreate
): Promise<IssuerRegistration> => {
  try {
    const response = await apiClient.post('/issuer-registrations', data);
    return response.data;
  } catch (error) {
    console.error('Error creating issuer registration:', error);
    throw error;
  }
};

export const getIssuerRegistration = async (
  id: string
): Promise<IssuerRegistration> => {
  try {
    const response = await apiClient.get(`/issuer-registrations/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching issuer registration:', error);
    throw error;
  }
};

export const getIssuerRegistrations = async (
  params: IssuerRegistrationListParams = {}
): Promise<IssuerRegistrationListResponse> => {
  try {
    const response = await apiClient.get('/issuer-registrations', {
      params,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching issuer registrations:', error);
    throw error;
  }
};

export const acceptIssuerRegistration = async (
  id: string
): Promise<IssuerRegistration> => {
  try {
    const response = await apiClient.patch(
      `/issuer-registrations/${id}/accept`
    );
    return response.data;
  } catch (error) {
    console.error('Error accepting issuer registration:', error);
    throw error;
  }
};

export const rejectIssuerRegistration = async (
  id: string
): Promise<IssuerRegistration> => {
  try {
    const response = await apiClient.patch(
      `/issuer-registrations/${id}/reject`
    );
    return response.data;
  } catch (error) {
    console.error('Error rejecting issuer registration:', error);
    throw error;
  }
};

export const deleteIssuerRegistration = async (
  id: string
): Promise<void> => {
  try {
    await apiClient.delete(`/issuer-registrations/${id}`);
  } catch (error) {
    console.error('Error deleting issuer registration:', error);
    throw error;
  }
};

/* =========================
   CERTIFICATE BLOCKCHAIN API
   ========================= */

export interface BlockchainCertificate {
  studentId: string;
  certHash: string;
  ipfsCID: string;
  isValid: boolean;
  timestampIssued: number;
  timestampLastUpdated: number;
  revokeReason: string;
}

export interface AllCertificatesResponse {
  success: boolean;
  certificates: BlockchainCertificate[];
  count: number;
}

export const getAllCertificatesFromBlockchain = async (): Promise<AllCertificatesResponse> => {
  try {
    const response = await apiClient.get('/certificate/blockchain/all');
    return response.data;
  } catch (error) {
    console.error('Error fetching certificates from blockchain:', error);
    throw error;
  }
};

export const verifyCertificateByNIM = async (studentId: string) => {
  const res = await apiClient.post('/certificate/verify', {
    student_id: studentId,
  })
  return res.data
}

// Add more API functions as needed
