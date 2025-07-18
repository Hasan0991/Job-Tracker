from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default='user')
    first_name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    jobs = relationship("Job", back_populates="user")
    applications = relationship("Application", back_populates="user")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    status = Column(String(50), default="sent")
    applied_at = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)
    
    user = relationship("User", back_populates="jobs")
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(255))
    website = Column(String(255))
    created_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, default=None)
    
    jobs = relationship("Job", back_populates="company")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    cover_letter = Column(Text)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=None)
    
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
