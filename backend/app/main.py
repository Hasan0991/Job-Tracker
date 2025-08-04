from fastapi import FastAPI
from app.routers import users, jobs, auth, protected, companies, applications
from app import models
from app.database import engine, Base,init_db 

app = FastAPI()

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
