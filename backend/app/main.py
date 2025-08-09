from fastapi import FastAPI
from app.routers import users, jobs, auth, protected, companies, applications
from app import models
from app.database import engine, Base,init_db 
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Job Tracker API",
    description="API for managing users, jobs, companies, and applications.",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT License",
    }
)
origins = [
    "http://localhost:3000",  # адрес твоего React (можешь добавить ещё если нужно)
    "https://your-frontend-domain.com",
    "*",  # если хочешь разрешить всем (для теста, но не рекомендовано на проде)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],  # разрешить все методы (POST, GET, PUT...)
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(auth.router)
app.include_router(protected.router)

@app.get("/")
def root():
    return {"message": "Job Tracker backend is running"}
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)