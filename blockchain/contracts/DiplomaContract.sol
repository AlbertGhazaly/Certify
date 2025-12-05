// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DiplomaContract {
    address public admin;

    struct Diploma {
        string cid;
        bool revoked;
    }

    mapping(address => Diploma[]) public diplomas;

    event DiplomaIssued(address indexed student, string cid);
    event DiplomaRevoked(address indexed student, uint256 index);

    constructor() {
        admin = msg.sender;
    }

    function issueDiploma(address student, string memory cid) external {
        require(msg.sender == admin, "Not authorized");
        diplomas[student].push(Diploma(cid, false));
        emit DiplomaIssued(student, cid);
    }

    function revokeDiploma(address student, uint256 index) external {
        require(msg.sender == admin, "Not authorized");
        diplomas[student][index].revoked = true;
        emit DiplomaRevoked(student, index);
    }

    function getDiplomas(address student) external view returns (Diploma[] memory) {
        return diplomas[student];
    }
}
