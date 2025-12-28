# 🎓 Certify - Blockchain-based Digital Certificate Management System

## 📝 Deskripsi

Certify adalah sistem manajemen sertifikat digital berbasis blockchain yang menggunakan teknologi kriptografi untuk menjamin keamanan dan keaslian ijazah/sertifikat. Sistem ini memanfaatkan Ethereum smart contract, IPFS untuk penyimpanan terdesentralisasi, dan tanda tangan digital multi-pihak untuk validasi sertifikat.

**Fitur Utama:**
- 🔐 Autentikasi berbasis kriptografi ECDSA
- ⛓️ Smart contract untuk pencatatan sertifikat di blockchain Sepolia
- 📦 Penyimpanan dokumen terdesentralisasi menggunakan IPFS
- ✍️ Multi-signature untuk penerbitan dan pencabutan sertifikat
- 🔍 Verifikasi keaslian sertifikat secara real-time

## 🚀 Cara Menjalankan

### Prasyarat
- Docker & Docker Compose
- Node.js v18+ (untuk development blockchain)
- MetaMask atau wallet Ethereum lainnya

### Langkah Instalasi

1. **Clone repository**
```bash
git clone <repository-url>
cd Certify
```

2. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env dan isi:
# - SEPOLIA_URL: RPC URL Sepolia testnet
# - CONTRACT_ADDRESS: Address smart contract yang sudah di-deploy
# - SECRET_KEY: Secret key untuk JWT authentication
```

3. **Jalankan dengan Docker Compose**
```bash
docker-compose up -d
```

4. **Akses aplikasi**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- IPFS Gateway: http://localhost:8080

### Deploy Smart Contract (Opsional)

```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
```

## ✨ Fitur Aplikasi

### 1. **Penerbitan Sertifikat**
- Upload dan enkripsi dokumen sertifikat (PDF)
- Penyimpanan file terenkripsi ke IPFS
- Proposal sertifikat oleh issuer
- Multi-signature signing untuk approval
- Pencatatan hash sertifikat ke blockchain

### 2. **Pencabutan Sertifikat**
- Proposal pencabutan dengan alasan
- Multi-signature untuk validasi pencabutan
- Update status di blockchain dengan timestamp

### 3. **Verifikasi Sertifikat**
- Verifikasi keaslian melalui blockchain
- Validasi tanda tangan digital issuer
- Pengecekan status (valid/revoked)
- Download dokumen dari IPFS

### 4. **Explorer**
- Daftar semua sertifikat yang diterbitkan
- Detail transaksi blockchain
- Riwayat penandatanganan
- Status real-time dari smart contract

## 🛠️ Teknologi & Dependencies

### Frontend (Vue.js + TypeScript)
```json
{
  "core": ["vue@3.5", "typescript@5.9", "vite@7.2"],
  "state": ["pinia@3.0", "vue-router@4.6"],
  "blockchain": ["ethers@5.8", "web3@4.3"],
  "crypto": ["crypto-js@4.2"],
  "storage": ["ipfs-http-client@56.0"],
  "http": ["axios@1.6"],
  "ui": ["tailwindcss@4.1", "lucide-vue-next"]
}
```

### Backend (FastAPI + Python)
```python
dependencies = [
    "FastAPI",           # Web framework
    "uvicorn",           # ASGI server
    "sqlalchemy",        # ORM
    "asyncpg",           # PostgreSQL async driver
    "pydantic",          # Data validation
    "web3",              # Ethereum interaction
    "ipfshttpclient",    # IPFS client
    "cryptography",      # Enkripsi/dekripsi
    "pycryptodome",      # Crypto utilities
    "ecdsa",             # Digital signature
    "eth-account",       # Ethereum account
    "python-jose",       # JWT tokens
    "passlib"            # Password hashing
]
```

### Blockchain (Hardhat)
```json
{
  "framework": "hardhat@2.27",
  "toolbox": "@nomicfoundation/hardhat-toolbox@6.1",
  "language": "Solidity ^0.8.20"
}
```

### Infrastructure
- **Database**: PostgreSQL 15
- **Storage**: IPFS (go-ipfs)
- **Blockchain**: Ethereum Sepolia Testnet
- **Containerization**: Docker & Docker Compose

## Role & Permission

| Role | Permissions |
|------|-------------|
| **Admin/Issuer** | Issue certificates, Sign proposals, Revoke certificates, Manage students |
| **Public** | View certificates, Verify authenticity |


## 👥 Members

| NIM | Pembagian Tugas | 
|------|-------------|
| **13522150** | Autentikasi, Issue/Revoke Certificate,Smart Contract |
| **13522151** | View&Verify Certificate, Smart Contract |
| **13522152** |  Sign Certificate (multi signature), Smart Contract|
