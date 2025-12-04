export namespace Validators {
  export function isValidEthereumAddress(address: string): boolean {
    return /^0x[a-fA-F0-9]{40}$/.test(address)
  }

  export function isValidHash(hash: string): boolean {
    return /^[a-fA-F0-9]{64}$/.test(hash)
  }

  export function isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  export function isValidStudentId(id: string): boolean {
    return /^\d{8}$/.test(id)
  }

  export function isValidDate(date: string): boolean {
    return !isNaN(Date.parse(date))
  }

  export function isValidCID(cid: string): boolean {
    return /^Qm[a-zA-Z0-9]{44}$/.test(cid) || /^bafy[a-zA-Z0-9]+$/.test(cid)
  }
}
