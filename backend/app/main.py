from fastapi import FastAPI
from app.routers import users,jobs,auth,protected,companies,applications
from app import models
from app.database import engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(auth.router)
app.include_router(protected.router)
@app.get("/")
def root():
    return {"message": "Job Tracker backend is running"}
