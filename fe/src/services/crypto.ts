import { generateKeyPairSync, privateKeyExport, publicKeyExport } from 'crypto';

export function generateECCKeys() {
    const { publicKey, privateKey } = generateKeyPairSync('ec', {
        namedCurve: 'secp256k1',
        publicKeyEncoding: {
            type: 'spki',
            format: 'pem'
        },
        privateKeyEncoding: {
            type: 'pkcs8',
            format: 'pem'
        }
    });

    return {
        publicKey,
        privateKey
    };
}

export function storePrivateKeyInLocalStorage(privateKey: string) {
    localStorage.setItem('privateKey', privateKey);
}

export function retrievePrivateKeyFromLocalStorage() {
    return localStorage.getItem('privateKey');
}

export function exportPublicKey(publicKey: string) {
    return publicKeyExport(publicKey, {
        type: 'spki',
        format: 'pem'
    });
}