# My Fullstack App

## 🔹 Overview
This project is a **fullstack web application** built with **React** (frontend) and **Python + FastAPI** (backend).  
It uses **PostgreSQL** for the database and is fully containerized with **Docker** for easy deployment.  
The app supports **JWT authentication** for secure user login and can be exposed via **ngrok** for testing or external access.

---

## 🛠️ Technologies
- **Frontend:** React, JavaScript, Axios  
- **Backend:** Python, FastAPI, SQLAlchemy  
- **Database:** PostgreSQL  
- **Authentication:** JWT (JSON Web Tokens)  
- **Dev Tools:** Docker, Docker Compose, ngrok  
- **Testing:** pytest  

---
## 📂 Project Structure
    my-fullstack-app/
    ├─ backend/
    │  ├─ app/
    │  │  ├─ main.py          # FastAPI app entry point
    │  │  ├─ models.py        # Database models (SQLAlchemy)
    │  │  ├─ database.py      # Database connection & initialization
    │  │  ├─ routers/         # API endpoints organized by feature
    │  │  └─ utils.py         # Utility functions (password hashing, JWT)
    │  ├─ requirements.txt    # Python dependencies
    │  └─ Dockerfile          # Backend Docker configuration
    │
    ├─ frontend/
    │  ├─ src/
    │  │  ├─ components/      # React components
    │  │  ├─ pages/           # Page views
    │  │  ├─ api/             # API service for backend calls
    │  │  └─ App.js           # Main React component
    │  ├─ package.json
    │  └─ Dockerfile          # Frontend Docker configuration
    │
    ├─ docker-compose.yml     # Defines services: frontend, backend, database
    └─ README.md


 
## Backend Setup (optional if using Docker)
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    pip install -r backend/requirements.txt
    uvicorn backend.app.main:app --reload
Open API docs: http://localhost:8000/docs

## Frontend Setup (optional if using Docker)
    cd frontend
    npm install
    npm start

Open browser at: http://localhost:3000

## Docker Setup
    docker-compose build
    docker-compose up


## Testing
    pip install pytest
    pytest tests/

## 🌐 Deployment

Deploy on Railway, Heroku, or any Docker-compatible server.

Temporary public URLs via ngrok:
