# Certify Project

## Overview
Certify is a full-stack application that combines a Vue.js frontend with a FastAPI backend. The frontend is built using Vite and TypeScript, while the backend is powered by FastAPI and connects to a PostgreSQL database. This project aims to provide a seamless user experience for managing cryptographic keys and user data.

## Project Structure
```
Certify
├── fe                  # Frontend application
│   ├── src            # Source files for Vue application
│   ├── public         # Public assets
│   ├── index.html     # Main HTML file
│   ├── package.json    # NPM configuration
│   ├── vite.config.ts  # Vite configuration
│   ├── tsconfig.json   # TypeScript configuration
│   └── Dockerfile      # Dockerfile for frontend
├── be                  # Backend application
│   ├── app            # FastAPI application files
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile      # Dockerfile for backend
├── docker-compose.yml  # Docker Compose configuration
├── .env                # Environment variables
└── README.md           # Project documentation
```

## Frontend Setup
The frontend is built using Vue.js with Vite for fast development and hot reloading. TypeScript is used for type safety and better development experience.

### Key Files
- **src/main.ts**: Entry point for the Vue application.
- **src/App.vue**: Root component of the application.
- **src/services/api.ts**: Handles API calls to the backend.
- **src/services/crypto.ts**: Contains cryptographic functions.
- **src/utils/localStorage.ts**: Utility functions for local storage management.

## Backend Setup
The backend is developed using FastAPI, providing a RESTful API for the frontend. It connects to a PostgreSQL database to manage user data.

### Database Schema
The PostgreSQL database includes a user table with the following fields:
- **role**: User's role in the application.
- **username**: Unique username for the user.
- **publicKeyX**: X coordinate of the user's public key.
- **publicKeyY**: Y coordinate of the user's public key.

### Key Files
- **app/main.py**: Entry point for the FastAPI application.
- **app/models/user.py**: Defines the User model.
- **app/schemas/user.py**: Pydantic schemas for user data validation.
- **app/services/sepolia.py**: Functions for interacting with the Sepolia network.

## Docker Configuration
The project uses Docker for containerization, allowing for easy deployment and management of the frontend and backend services. The `docker-compose.yml` file defines the services and networking between them.

## Installation and Usage
1. Clone the repository.
2. Navigate to the project directory.
3. Create a `.env` file with the necessary environment variables for the backend.
4. Run `docker-compose up` to start the application.
5. Access the frontend at `http://localhost:3000` and the backend at `http://localhost:8000`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.