// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DiplomaContract {
    // Issuer structure
    struct Issuer {
        address walletId;
        string publicKey; // hex string of public key
        bool isActive;
    }

    // Certificate structure
    struct Certificate {
        string studentId; // NIM or student ID
        bytes32 certHash; // hash of certificate content
        string ipfsCID; // IPFS CID of the PDF
        address[] issuerWallets; // list of issuer wallet addresses
        mapping(address => bytes) issueSignatures; // issuer address => signature for issuance
        mapping(address => bytes) revokeSignatures; // issuer address => signature for revocation
        uint256 issueSignatureCount;
        uint256 revokeSignatureCount;
        bool isValid; // valid/invalid status
        uint256 timestampIssued;
        uint256 timestampLastUpdated;
        string revokeReason;
        bool requiresAllSignatures; // if true, requires all issuers to sign
    }

    // Mappings
    mapping(address => Issuer) private issuers;
    address[] private issuerList;
    
    mapping(string => Certificate) private certificates; // studentId => Certificate
    mapping(string => bool) private certificateExists; // studentId => exists
    string[] private certificateIds; // Array to store all certificate IDs

    // Events
    event IssuerAdded(address indexed walletId, string publicKey);
    event IssuerRemoved(address indexed walletId);
    event IssuerPublicKeyUpdated(address indexed walletId, string newPublicKey);
    event CertificateProposed(string indexed studentId, bytes32 certHash, string ipfsCID, address indexed proposer);
    event CertificateIssueSigned(string indexed studentId, address indexed issuer);
    event CertificateIssued(string indexed studentId, bytes32 certHash, string ipfsCID);
    event CertificateRevokeSigned(string indexed studentId, address indexed issuer, string reason);
    event CertificateRevoked(string indexed studentId, string reason);

    // Modifiers
    modifier onlyIssuer() {
        require(issuers[msg.sender].isActive, "Only issuer can perform this action");
        _;
    }

    modifier onlyActiveIssuerForCert(string memory studentId) {
        require(certificateExists[studentId], "Certificate does not exist");
        bool isIssuerForCert = false;
        Certificate storage cert = certificates[studentId];
        for (uint i = 0; i < cert.issuerWallets.length; i++) {
            if (cert.issuerWallets[i] == msg.sender) {
                isIssuerForCert = true;
                break;
            }
        }
        require(isIssuerForCert && issuers[msg.sender].isActive, "Not an authorized issuer for this certificate");
        _;
    }

    constructor() {
        // Initialize the three default issuers
        address albert = 0x9025bCF725Cce60610030A4824156346fDFAc97c;
        address roihan = 0xd924c8F1BA5f69292baDD9baf06893D7F90aeBCd;
        address samy = 0xda2486286e253201de026A066f75Bb8B0696E8cD;

        issuers[albert] = Issuer({
            walletId: albert,
            publicKey: "",
            isActive: true
        });
        issuerList.push(albert);

        issuers[roihan] = Issuer({
            walletId: roihan,
            publicKey: "",
            isActive: true
        });
        issuerList.push(roihan);

        issuers[samy] = Issuer({
            walletId: samy,
            publicKey: "",
            isActive: true
        });
        issuerList.push(samy);
    }

    // ========== ISSUER MANAGEMENT ==========

    /**
     * @dev Add a new issuer (only existing issuers can add)
     * @param walletId Address of the issuer
     * @param publicKey Hex string of issuer's public key
     */
    function addIssuer(address walletId, string memory publicKey) external onlyIssuer {
        require(!issuers[walletId].isActive, "Issuer already exists");
        require(walletId != address(0), "Invalid wallet address");
        
        issuers[walletId] = Issuer({
            walletId: walletId,
            publicKey: publicKey,
            isActive: true
        });
        
        issuerList.push(walletId);
        emit IssuerAdded(walletId, publicKey);
    }

    /**
     * @dev Remove an issuer (only existing issuers can remove)
     * @param walletId Address of the issuer to remove
     */
    function removeIssuer(address walletId) external onlyIssuer {
        require(issuers[walletId].isActive, "Issuer does not exist");
        
        // Count active issuers
        uint256 activeCount = 0;
        for (uint i = 0; i < issuerList.length; i++) {
            if (issuers[issuerList[i]].isActive) {
                activeCount++;
            }
        }
        require(activeCount > 1, "Cannot remove last issuer");
        
        issuers[walletId].isActive = false;
        emit IssuerRemoved(walletId);
    }

    /**
     * @dev Update issuer's public key (only the same wallet address can update their own key)
     * @param newPublicKey New public key hex string
     */
    function updateIssuerPublicKey(string memory newPublicKey) external onlyIssuer {
        require(issuers[msg.sender].isActive, "Issuer does not exist");
        
        issuers[msg.sender].publicKey = newPublicKey;
        emit IssuerPublicKeyUpdated(msg.sender, newPublicKey);
    }

    /**
     * @dev Get list of all issuer addresses
     */
    function getIssuerList() external view returns (address[] memory) {
        return issuerList;
    }

    /**
     * @dev Get issuer details
     */
    function getIssuer(address walletId) external view returns (Issuer memory) {
        return issuers[walletId];
    }

    /**
     * @dev Check if an address is an active issuer (for backend compatibility)
     */
    function isIssuer(address walletId) external view returns (bool) {
        return issuers[walletId].isActive;
    }

    // ========== CERTIFICATE MANAGEMENT ==========

    /**
     * @dev Propose a new certificate (only issuer can propose)
     * @param studentId Student NIM or ID
     * @param certHash Hash of the certificate content
     * @param ipfsCID IPFS CID of the PDF certificate
     * @param issuerWallets List of issuer wallet addresses who need to sign
     * @param signature First issuer's signature
     * @param requiresAllSignatures If true, all issuers must sign; if false, majority is enough
     */
    function proposeCertificate(
        string memory studentId,
        bytes32 certHash,
        string memory ipfsCID,
        address[] memory issuerWallets,
        bytes memory signature,
        bool requiresAllSignatures
    ) external onlyIssuer {
        require(bytes(studentId).length > 0, "Invalid student ID");
        require(issuerWallets.length > 0, "At least one issuer required");
        require(bytes(ipfsCID).length > 0, "IPFS CID cannot be empty");
        
        // If certificate exists and is revoked, delete it first
        if (certificateExists[studentId] && !certificates[studentId].isValid) {
            delete certificates[studentId];
        }
        
        require(!certificateExists[studentId], "Certificate already exists for this student ID");
        
        // Validate all issuers are active
        bool proposerIsInList = false;
        for (uint i = 0; i < issuerWallets.length; i++) {
            require(issuers[issuerWallets[i]].isActive, "One or more issuers are not active");
            if (issuerWallets[i] == msg.sender) {
                proposerIsInList = true;
            }
        }
        require(proposerIsInList, "Proposer must be in issuer list");
        
        Certificate storage cert = certificates[studentId];
        cert.studentId = studentId;
        cert.certHash = certHash;
        cert.ipfsCID = ipfsCID;
        cert.issuerWallets = issuerWallets;
        cert.issueSignatureCount = 1;
        cert.revokeSignatureCount = 0;
        cert.isValid = false; // Not valid until all required signatures are collected
        cert.timestampIssued = block.timestamp;
        cert.timestampLastUpdated = block.timestamp;
        cert.revokeReason = "";
        cert.requiresAllSignatures = requiresAllSignatures;
        cert.issueSignatures[msg.sender] = signature;
        
        certificateExists[studentId] = true;
        certificateIds.push(studentId); // Add to certificate IDs list
        
        emit CertificateProposed(studentId, certHash, ipfsCID, msg.sender);
        emit CertificateIssueSigned(studentId, msg.sender);
        
        // Check if certificate should be automatically issued
        _checkAndIssueCertificate(studentId);
    }

    /**
     * @dev Sign a certificate for issuance (only authorized issuers can sign)
     * @param studentId Student NIM or ID
     * @param signature ECDSA signature from the issuer
     */
    function signCertificateIssuance(
        string memory studentId,
        bytes memory signature
    ) external onlyActiveIssuerForCert(studentId) {
        Certificate storage cert = certificates[studentId];
        require(!cert.isValid, "Certificate already issued");
        require(cert.issueSignatures[msg.sender].length == 0, "Already signed by this issuer");
        
        cert.issueSignatures[msg.sender] = signature;
        cert.issueSignatureCount++;
        cert.timestampLastUpdated = block.timestamp;
        
        emit CertificateIssueSigned(studentId, msg.sender);
        
        // Check if certificate should be issued
        _checkAndIssueCertificate(studentId);
    }

    /**
     * @dev Internal function to check if certificate has enough signatures and issue it
     * @param studentId Student NIM or ID
     */
    function _checkAndIssueCertificate(string memory studentId) internal {
        Certificate storage cert = certificates[studentId];
        
        bool shouldIssue = false;
        if (cert.requiresAllSignatures) {
            // Requires all issuers to sign
            shouldIssue = cert.issueSignatureCount == cert.issuerWallets.length;
        } else {
            // Requires majority (more than half)
            shouldIssue = cert.issueSignatureCount > cert.issuerWallets.length / 2;
        }
        
        if (shouldIssue && !cert.isValid) {
            cert.isValid = true;
            cert.timestampLastUpdated = block.timestamp;
            emit CertificateIssued(studentId, cert.certHash, cert.ipfsCID);
        }
    }

    /**
     * @dev Sign to revoke a certificate (only authorized issuers can sign)
     * @param studentId Student NIM or ID
     * @param reason Reason for revocation
     * @param signature ECDSA signature from the issuer
     */
    function signCertificateRevocation(
        string memory studentId,
        string memory reason,
        bytes memory signature
    ) external onlyActiveIssuerForCert(studentId) {
        Certificate storage cert = certificates[studentId];
        require(cert.isValid, "Certificate is not valid or already revoked");
        require(cert.revokeSignatures[msg.sender].length == 0, "Already signed revocation by this issuer");
        
        cert.revokeSignatures[msg.sender] = signature;
        cert.revokeSignatureCount++;
        cert.timestampLastUpdated = block.timestamp;
        
        // Store reason (last one provided)
        if (bytes(reason).length > 0) {
            cert.revokeReason = reason;
        }
        
        emit CertificateRevokeSigned(studentId, msg.sender, reason);
        
        // Check if certificate should be revoked
        _checkAndRevokeCertificate(studentId);
    }

    /**
     * @dev Internal function to check if certificate has enough revocation signatures
     * @param studentId Student NIM or ID
     */
    function _checkAndRevokeCertificate(string memory studentId) internal {
        Certificate storage cert = certificates[studentId];
        
        bool shouldRevoke = false;
        if (cert.requiresAllSignatures) {
            // Requires all issuers to sign
            shouldRevoke = cert.revokeSignatureCount == cert.issuerWallets.length;
        } else {
            // Requires majority (more than half)
            shouldRevoke = cert.revokeSignatureCount > cert.issuerWallets.length / 2;
        }
        
        if (shouldRevoke && cert.isValid) {
            cert.isValid = false;
            cert.timestampLastUpdated = block.timestamp;
            emit CertificateRevoked(studentId, cert.revokeReason);
        }
    }

    /**
     * @dev Get certificate details
     * @param studentId Student NIM or ID
     */
    function getCertificate(string memory studentId) external view returns (
        string memory _studentId,
        bytes32 certHash,
        string memory ipfsCID,
        address[] memory issuerWallets,
        uint256 issueSignatureCount,
        uint256 revokeSignatureCount,
        bool isValid,
        uint256 timestampIssued,
        uint256 timestampLastUpdated,
        string memory revokeReason,
        bool requiresAllSignatures
    ) {
        require(certificateExists[studentId], "Certificate does not exist");
        Certificate storage cert = certificates[studentId];
        return (
            cert.studentId,
            cert.certHash,
            cert.ipfsCID,
            cert.issuerWallets,
            cert.issueSignatureCount,
            cert.revokeSignatureCount,
            cert.isValid,
            cert.timestampIssued,
            cert.timestampLastUpdated,
            cert.revokeReason,
            cert.requiresAllSignatures
        );
    }

    /**
     * @dev Get all certificates (both valid and revoked)
     * Returns arrays of certificate data for all certificates
     */
    function getAllCertificates() external view returns (
        string[] memory studentIds,
        bytes32[] memory certHashes,
        string[] memory ipfsCIDs,
        bool[] memory isValids,
        uint256[] memory timestampsIssued,
        uint256[] memory timestampsLastUpdated,
        string[] memory revokeReasons
    ) {
        uint256 totalCerts = certificateIds.length;
        
        studentIds = new string[](totalCerts);
        certHashes = new bytes32[](totalCerts);
        ipfsCIDs = new string[](totalCerts);
        isValids = new bool[](totalCerts);
        timestampsIssued = new uint256[](totalCerts);
        timestampsLastUpdated = new uint256[](totalCerts);
        revokeReasons = new string[](totalCerts);
        
        for (uint i = 0; i < totalCerts; i++) {
            string memory studentId = certificateIds[i];
            Certificate storage cert = certificates[studentId];
            
            studentIds[i] = cert.studentId;
            certHashes[i] = cert.certHash;
            ipfsCIDs[i] = cert.ipfsCID;
            isValids[i] = cert.isValid;
            timestampsIssued[i] = cert.timestampIssued;
            timestampsLastUpdated[i] = cert.timestampLastUpdated;
            revokeReasons[i] = cert.revokeReason;
        }
        
        return (studentIds, certHashes, ipfsCIDs, isValids, timestampsIssued, timestampsLastUpdated, revokeReasons);
    }

    /**
     * @dev Get total number of certificates
     */
    function getCertificateCount() external view returns (uint256) {
        return certificateIds.length;
    }

    /**
     * @dev Get issue signature for a specific issuer
     * @param studentId Student NIM or ID
     * @param issuer Address of the issuer
     */
    function getIssueSignature(
        string memory studentId,
        address issuer
    ) external view returns (bytes memory) {
        require(certificateExists[studentId], "Certificate does not exist");
        return certificates[studentId].issueSignatures[issuer];
    }

    /**
     * @dev Get revoke signature for a specific issuer
     * @param studentId Student NIM or ID
     * @param issuer Address of the issuer
     */
    function getRevokeSignature(
        string memory studentId,
        address issuer
    ) external view returns (bytes memory) {
        require(certificateExists[studentId], "Certificate does not exist");
        return certificates[studentId].revokeSignatures[issuer];
    }

    /**
     * @dev Check if certificate exists
     * @param studentId Student NIM or ID
     */
    function certificateExistsFor(string memory studentId) external view returns (bool) {
        return certificateExists[studentId];
    }

    /**
     * @dev Check if certificate is valid
     * @param studentId Student NIM or ID
     */
    function isCertificateValid(string memory studentId) external view returns (bool) {
        if (!certificateExists[studentId]) {
            return false;
        }
        return certificates[studentId].isValid;
    }
}