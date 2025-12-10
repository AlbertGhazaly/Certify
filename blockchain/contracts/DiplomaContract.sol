// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DiplomaContract {
    // Multiple institutions instead of single institution
    mapping(address => bool) private institutions;
    address[] private institutionList;

    // Admin structure
    struct Admin {
        address walletId;
        string publicKey; // hex string of public key
        bool isActive;
    }

    // Student structure
    struct Student {
        address walletId;
        bytes32 hashedIdentity; // hash_sha256(NIM, Nama, nonce)
        bool isActive;
    }

    // Certificate structure
    struct Certificate {
        bytes32 certHash; // hash of certificate content
        address[] issuerWallets; // list of issuer wallet addresses
        mapping(address => bytes) signatures; // issuer address => signature
        uint256 signatureCount;
        bool isValid; // valid/invalid status
        uint256 timestampIssued;
        uint256 timestampLastUpdated;
        string revokeReason;
    }

    // Mappings - use private for better encapsulation
    mapping(address => Admin) private admins;
    address[] private adminList;
    
    mapping(address => Student) private students;
    address[] private studentList;
    
    mapping(address => mapping(uint256 => Certificate)) private certificates;
    mapping(address => uint256) private certificateCount;

    // Events
    event AdminAdded(address indexed walletId, string publicKey);
    event AdminRemoved(address indexed walletId);
    event StudentAdded(address indexed walletId, bytes32 hashedIdentity);
    event StudentRemoved(address indexed walletId);
    event CertificateIssued(address indexed student, uint256 indexed certIndex, bytes32 certHash);
    event CertificateSigned(address indexed student, uint256 indexed certIndex, address indexed issuer);
    event CertificateRevoked(address indexed student, uint256 indexed certIndex, string reason);
    event InstitutionAdded(address indexed walletId);
    event InstitutionRemoved(address indexed walletId);

    // Modifiers
    modifier onlyInstitution() {
        require(institutions[msg.sender], "Only institution can perform this action");
        _;
    }

    modifier onlyAdmin() {
        require(admins[msg.sender].isActive, "Only admin can perform this action");
        _;
    }

    modifier onlyActiveIssuer(address student, uint256 certIndex) {
        bool isIssuer = false;
        Certificate storage cert = certificates[student][certIndex];
        for (uint i = 0; i < cert.issuerWallets.length; i++) {
            if (cert.issuerWallets[i] == msg.sender) {
                isIssuer = true;
                break;
            }
        }
        require(isIssuer && admins[msg.sender].isActive, "Not an authorized issuer for this certificate");
        _;
    }

    constructor() {
        // Initialize the three institutions
        address albert = 0x9025bCF725Cce60610030A4824156346fDFAc97c;
        address roihan = 0xd924c8F1BA5f69292baDD9baf06893D7F90aeBCd;
        address samy = 0xda2486286e253201de026A066f75Bb8B0696E8cD;

        institutions[albert] = true;
        institutions[roihan] = true;
        institutions[samy] = true;

        institutionList.push(albert);
        institutionList.push(roihan);
        institutionList.push(samy);
    }

    // ========== INSTITUTION MANAGEMENT ==========

    /**
     * @dev Get list of all institution addresses
     */
    function getInstitutionList() external view returns (address[] memory) {
        return institutionList;
    }

    /**
     * @dev Check if an address is an institution
     */
    function isInstitution(address walletId) external view returns (bool) {
        return institutions[walletId];
    }

    /**
     * @dev Add a new institution (only existing institutions can add)
     */
    function addInstitution(address walletId) external onlyInstitution {
        require(walletId != address(0), "Invalid address");
        require(!institutions[walletId], "Already an institution");
        
        institutions[walletId] = true;
        institutionList.push(walletId);
        emit InstitutionAdded(walletId);
    }

    /**
     * @dev Remove an institution (only existing institutions can remove)
     * Cannot remove if it would leave zero institutions
     */
    function removeInstitution(address walletId) external onlyInstitution {
        require(institutions[walletId], "Not an institution");
        
        // Count active institutions
        uint256 activeCount = 0;
        for (uint i = 0; i < institutionList.length; i++) {
            if (institutions[institutionList[i]]) {
                activeCount++;
            }
        }
        require(activeCount > 1, "Cannot remove last institution");

        institutions[walletId] = false;
        emit InstitutionRemoved(walletId);
    }

    // ========== ADMIN MANAGEMENT ==========

    /**
     * @dev Add a new admin (only institution can add)
     * @param walletId Address of the admin
     * @param publicKey Hex string of admin's public key
     */
    function addAdmin(address walletId, string memory publicKey) external onlyInstitution {
        require(!admins[walletId].isActive, "Admin already exists");
        require(walletId != address(0), "Invalid wallet address");
        
        admins[walletId] = Admin({
            walletId: walletId,
            publicKey: publicKey,
            isActive: true
        });
        
        adminList.push(walletId);
        emit AdminAdded(walletId, publicKey);
    }

    /**
     * @dev Remove an admin (only institution can remove)
     * @param walletId Address of the admin to remove
     */
    function removeAdmin(address walletId) external onlyInstitution {
        require(admins[walletId].isActive, "Admin does not exist");
        
        admins[walletId].isActive = false;
        emit AdminRemoved(walletId);
    }

    /**
     * @dev Get list of all admin addresses
     */
    function getAdminList() external view returns (address[] memory) {
        return adminList;
    }

    /**
     * @dev Get admin details
     */
    function getAdmin(address walletId) external view returns (Admin memory) {
        return admins[walletId];
    }

    /**
     * @dev Check if an address is an active admin
     */
    function isAdmin(address walletId) external view returns (bool) {
        return admins[walletId].isActive;
    }

    // ========== STUDENT MANAGEMENT ==========

    /**
     * @dev Add a new student (only admin can add)
     * @param walletId Address of the student
     * @param hashedIdentity Pre-computed hash of SHA256(NIM, Nama, nonce)
     */
    function addStudent(address walletId, bytes32 hashedIdentity) external onlyAdmin {
        require(!students[walletId].isActive, "Student already exists");
        require(walletId != address(0), "Invalid wallet address");
        
        students[walletId] = Student({
            walletId: walletId,
            hashedIdentity: hashedIdentity,
            isActive: true
        });
        
        studentList.push(walletId);
        emit StudentAdded(walletId, hashedIdentity);
    }

    /**
     * @dev Remove a student (only admin can remove)
     * @param walletId Address of the student to remove
     */
    function removeStudent(address walletId) external onlyAdmin {
        require(students[walletId].isActive, "Student does not exist");
        
        students[walletId].isActive = false;
        emit StudentRemoved(walletId);
    }

    /**
     * @dev Get list of all student addresses
     */
    function getStudentList() external view returns (address[] memory) {
        return studentList;
    }

    /**
     * @dev Get student details
     */
    function getStudent(address walletId) external view returns (Student memory) {
        return students[walletId];
    }

    /**
     * @dev Check if an address is an active student
     */
    function isStudent(address walletId) external view returns (bool) {
        return students[walletId].isActive;
    }

    // ========== CERTIFICATE MANAGEMENT ==========

    /**
     * @dev Issue a new certificate (only admin can issue)
     * @param student Address of the student
     * @param certHash Hash of the certificate content
     * @param issuerWallets List of issuer wallet addresses who need to sign
     */
    function issueCertificate(
        address student,
        bytes32 certHash,
        address[] memory issuerWallets
    ) external onlyAdmin {
        require(students[student].isActive, "Student does not exist or inactive");
        require(issuerWallets.length > 0, "At least one issuer required");
        
        // Validate all issuers are active admins
        for (uint i = 0; i < issuerWallets.length; i++) {
            require(admins[issuerWallets[i]].isActive, "One or more issuers are not active admins");
        }
        
        uint256 certIndex = certificateCount[student];
        Certificate storage cert = certificates[student][certIndex];
        
        cert.certHash = certHash;
        cert.issuerWallets = issuerWallets;
        cert.signatureCount = 0;
        cert.isValid = true;
        cert.timestampIssued = block.timestamp;
        cert.timestampLastUpdated = block.timestamp;
        cert.revokeReason = "";
        
        certificateCount[student]++;
        emit CertificateIssued(student, certIndex, certHash);
    }

    /**
     * @dev Sign a certificate (only authorized issuers can sign)
     * @param student Address of the student
     * @param certIndex Index of the certificate
     * @param signature ECDSA signature from the issuer
     */
    function signCertificate(
        address student,
        uint256 certIndex,
        bytes memory signature
    ) external onlyActiveIssuer(student, certIndex) {
        Certificate storage cert = certificates[student][certIndex];
        require(cert.isValid, "Certificate is revoked");
        require(cert.signatures[msg.sender].length == 0, "Already signed by this issuer");
        
        cert.signatures[msg.sender] = signature;
        cert.signatureCount++;
        cert.timestampLastUpdated = block.timestamp;
        
        emit CertificateSigned(student, certIndex, msg.sender);
    }

    /**
     * @dev Revoke a certificate (only authorized issuers can revoke)
     * @param student Address of the student
     * @param certIndex Index of the certificate
     * @param reason Reason for revocation
     * @param signature Signature from the issuer
     */
    function revokeCertificate(
        address student,
        uint256 certIndex,
        string memory reason,
        bytes memory signature
    ) external onlyActiveIssuer(student, certIndex) {
        Certificate storage cert = certificates[student][certIndex];
        require(cert.isValid, "Certificate already revoked");
        
        cert.isValid = false;
        cert.revokeReason = reason;
        cert.signatures[msg.sender] = signature;
        cert.timestampLastUpdated = block.timestamp;
        
        emit CertificateRevoked(student, certIndex, reason);
    }

    /**
     * @dev Get certificate details
     * @param student Address of the student
     * @param certIndex Index of the certificate
     */
    function getCertificate(address student, uint256 certIndex) external view returns (
        bytes32 certHash,
        address[] memory issuerWallets,
        uint256 signatureCount,
        bool isValid,
        uint256 timestampIssued,
        uint256 timestampLastUpdated,
        string memory revokeReason
    ) {
        Certificate storage cert = certificates[student][certIndex];
        return (
            cert.certHash,
            cert.issuerWallets,
            cert.signatureCount,
            cert.isValid,
            cert.timestampIssued,
            cert.timestampLastUpdated,
            cert.revokeReason
        );
    }

    /**
     * @dev Get signature for a specific issuer
     * @param student Address of the student
     * @param certIndex Index of the certificate
     * @param issuer Address of the issuer
     */
    function getSignature(
        address student,
        uint256 certIndex,
        address issuer
    ) external view returns (bytes memory) {
        return certificates[student][certIndex].signatures[issuer];
    }

    /**
     * @dev Verify if all required signatures are present
     * @param student Address of the student
     * @param certIndex Index of the certificate
     */
    function isFullySigned(address student, uint256 certIndex) external view returns (bool) {
        Certificate storage cert = certificates[student][certIndex];
        return cert.signatureCount == cert.issuerWallets.length;
    }

    /**
     * @dev Get number of certificates for a student
     * @param student Address of the student
     */
    function getStudentCertificateCount(address student) external view returns (uint256) {
        return certificateCount[student];
    }
}