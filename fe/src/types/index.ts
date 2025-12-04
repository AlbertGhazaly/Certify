export interface User {
    id: number;
    role: string;
    username: string;
    publicKeyX: string;
    publicKeyY: string;
}

export interface AuthResponse {
    accessToken: string;
    refreshToken: string;
}

export interface LocalStorageKeys {
    privateKey: string;
    user: string;
}

export interface IPFSResponse {
    cid: string;
    path: string;
}