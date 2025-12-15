export interface User {
  address: string
  role: "issuer"
  isAuthenticated: boolean
}

export interface AuthResponse {
  success: boolean
  message: string
  session_token?: string
  jwt_token?: string
  role?: string
  wallet_address?: string
}

export interface ChallengeResponse {
  challenge: string
  nonce: string
}

export interface LocalStorageKeys {
    privateKey: string;
    user: string;
}

export interface IPFSResponse {
    cid: string;
    path: string;
}


export interface Certificate {
  id: string
  studentName: string
  studentId: string
  institution: string
  degree: string
  issueDate: string
  signatureHash: string
  documentHash: string
  ipfsCid: string
  issuerAddress: string
  status: "active" | "revoked"
  createdAt: string
}

export interface Transaction {
  id: string
  hash: string
  previousHash: string
  type: "issue" | "revoke" | "update"
  certificateId: string
  issuerAddress: string
  data: Record<string, unknown>
  signature: string
  timestamp: string
  blockNumber: number
}

export interface IssueCertificatePayload {
  studentName: string
  studentId: string
  degree: string
  birthPlace: string
  birthDate: string
  documentHash: string
  ipfsCid: string
  encryptionKey: string
}

export interface RevokeCertificatePayload {
  certificateId: string
  reason: string
}

export interface WalletAuthChallenge {
  nonce: string
  expiresAt: number
}

export interface BlockchainTransaction {
  type: string
  certificateId?: string
  data: Record<string, unknown>
  signature: string
  timestamp: number
}

export interface VerificationResult {
  isValid: boolean
  certificate: Certificate | null
  errors: string[]
}

export interface Student {
  nim: string
  nama: string
  wallet_address: string
}

export interface StudentCreate {
  nim: string
  nama: string
  wallet_address: string
}

export type IssuerStatus = 'pending' | 'accept' | 'reject';

export interface IssuerRegistration {
  id_registration: string;
  name: string;
  wallet_address: string;
  public_key_x: string;
  public_key_y: string;
  created_at: number;
  status: IssuerStatus;
}

export interface IssuerRegistrationCreate {
  name: string;
  wallet_address: string;
  // public_key_x: string;
  // public_key_y: string;
}

export interface IssuerRegistrationListResponse {
  total: number;
  page: number;
  page_size: number;
  items: IssuerRegistration[];
}

export interface IssuerRegistrationListParams {
  name?: string;
  status?: IssuerStatus;
  start_date?: number;
  end_date?: number;
  sort?: 'latest' | 'oldest';
  page?: number;
  page_size?: number;
}
