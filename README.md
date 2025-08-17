My Fullstack App

🔹 Overview

This project is a fullstack web application built with React for the frontend and Python + FastAPI for the backend.It uses PostgreSQL as the database and is fully containerized with Docker for easy deployment.The app also supports JWT authentication for secure user login and can be exposed via ngrok for testing or external access.

🛠️ Technologies

Frontend: React, JavaScript, Axios (for API calls)

Backend: Python, FastAPI, SQLAlchemy

Database: PostgreSQL

Authentication: JWT (JSON Web Tokens)

Dev Tools: Docker, Docker Compose, ngrok

Testing: pytest

📂 Project Structure

my-fullstack-app/
├─ backend/
│  ├─ app/
│  │  ├─ main.py           # FastAPI app entry point
│  │  ├─ models.py         # Database models (SQLAlchemy)
│  │  ├─ database.py       # Database connection and initialization
│  │  ├─ routers/          # API endpoints organized by feature
│  │  └─ utils.py          # Utility functions (password hashing, JWT)
│  ├─ requirements.txt     # Python dependencies
│  └─ Dockerfile           # Backend Docker configuration
│
├─ frontend/
│  ├─ src/
│  │  ├─ components/       # React components
│  │  ├─ pages/            # Page views
│  │  ├─ api/              # API service for backend calls
│  │  └─ App.js            # Main React component
│  ├─ package.json
│  └─ Dockerfile           # Frontend Docker configuration
│
├─ docker-compose.yml      # Defines services: frontend, backend, database
└─ README.md

🚀 Setup & Run

1. Clone the repository

git clone https://github.com/yourusername/my-fullstack-app.git
cd my-fullstack-app

2. Backend Setup

Create a virtual environment (optional):

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

Install dependencies:

pip install -r backend/requirements.txt

Start FastAPI backend:

uvicorn backend.app.main:app --reload

Check API at: http://localhost:8000/docs

3. Frontend Setup

Navigate to the frontend folder:

cd frontend

Install dependencies:

npm install

Run React development server:

npm start

Open browser at: http://localhost:3000

4. Docker Setup

The app is fully containerized using Docker and Docker Compose.

Build containers:

docker-compose build

Run containers:

docker-compose up

Access:

Backend: http://localhost:8000/docs

Frontend: http://localhost:3000

5. Testing

Install pytest:

pip install pytest

Run tests:

pytest tests/

🔐 Authentication

Users can register and log in using JWT authentication.

The backend issues a JWT token after successful login.

React frontend stores this token in localStorage and attaches it to API requests for protected routes.

🗃️ Database

PostgreSQL is used for persistent storage.

SQLAlchemy handles database interactions and migrations.

Tables include users, jobs, applications, and companies.

🌐 Deployment

The app can be deployed using Railway, Heroku, or any Docker-compatible server.

ngrok can be used for temporary public URLs during development:

ngrok http 8000  # exposes backend

📌 Notes

Make sure .env or config files have proper database credentials.

Update BASE_URL in frontend API service to match backend URL when deployed.

Enable CORS in FastAPI if frontend is served from a different domain.

