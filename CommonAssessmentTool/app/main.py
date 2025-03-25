"""
Main application module for the Common Assessment Tool.
This module initializes the FastAPI application and includes all routers.
Handles database initialization and CORS middleware configuration.
"""

from fastapi import FastAPI
from app import models
from app.database import engine
from app.clients.router import router as clients_router
from app.auth.router import router as auth_router
from app.clients.ml.models.ml_router import router as ml_router 
from app.clients.ml.models.model_manager import ModelManager         
from fastapi.middleware.cors import CORSMiddleware

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(title="Case Management API", description="API for managing client cases", version="1.0.0")

# Load ML models on startup
ModelManager.load_models()

# Include routers
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(ml_router)  

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_methods=["*"],   
    allow_headers=["*"],     
    allow_credentials=True,
)
