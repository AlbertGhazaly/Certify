/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_IPFS_GATEWAY: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

// MetaMask Ethereum Provider
declare global {
  interface Window {
    ethereum?: {
      request: (args: { method: string; params?: any[] }) => Promise<any>
      on: (event: string, callback: (...args: any[]) => void) => void
      removeListener: (event: string, callback: (...args: any[]) => void) => void
      removeAllListeners: (event: string) => void
      selectedAddress: string | null
      isMetaMask?: boolean
      chainId?: string
      networkVersion?: string
    }
  }
}

export {}