# My Fullstack App

## 🔹 Overview
This project is a fullstack web application built with **React** (frontend) and **Python + FastAPI** (backend).  
It uses **PostgreSQL** (or MongoDB) for the database. The app is containerized with **Docker** and can be exposed via **ngrok** for external access.

---

## 🛠️ Technologies
- **Frontend:** React
- **Backend:** Python,FastAPI
- **Database:** PostgreSQL 
- **Dev Tools:** Docker, Docker Compose, ngrok
- **Authentication:** JWT (JSON Web Tokens)

---

## 🚀 Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/my-fullstack-app.git
cd my-fullstack-app

## Testing

To run tests for the application, you can use pytest to verify that all your endpoints work as expected:

Install pytest:

    pip install pytest

Run tests:

    pytest tests/

## Docker Setup

This project is containerized with Docker to run both the Flask application and MySQL database in isolated environments.
Build the Docker containers:

    docker-compose build

Run the containers:

    docker-compose up
