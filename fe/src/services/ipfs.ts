import { create } from 'ipfs-http-client';

const ipfs = create({ url: 'https://ipfs.infura.io:5001/api/v0' });

export const uploadFileToIPFS = async (file: File) => {
    try {
        const added = await ipfs.add(file);
        return added.path;
    } catch (error) {
        console.error('Error uploading file to IPFS:', error);
        throw error;
    }
};

export const retrieveFileFromIPFS = async (cid: string) => {
    try {
        const stream = ipfs.cat(cid);
        let data = '';

        for await (const chunk of stream) {
            data += new TextDecoder().decode(chunk);
        }

        return data;
    } catch (error) {
        console.error('Error retrieving file from IPFS:', error);
        throw error;
    }
};